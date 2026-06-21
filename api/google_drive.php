<?php

/**
 * Minimal Google Drive v3 client for shared-hosting PHP.
 * It intentionally has no Composer dependency: service-account JWT signing uses
 * OpenSSL and HTTP requests use cURL (with a stream fallback).
 */

function drive_base64url(string $value): string
{
    return rtrim(strtr(base64_encode($value), '+/', '-_'), '=');
}

function drive_credentials(): array
{
    $raw = defined('GOOGLE_DRIVE_CREDENTIALS_JSON') ? trim((string)GOOGLE_DRIVE_CREDENTIALS_JSON) : '';
    if ($raw === '') {
        throw new RuntimeException('Chưa cấu hình GOOGLE_DRIVE_CREDENTIALS_JSON trên hosting.');
    }
    $credentials = json_decode($raw, true);
    $oauthClient = $credentials['installed'] ?? $credentials['web'] ?? null;
    $isServiceAccount = !empty($credentials['client_email']) && !empty($credentials['private_key']);
    if (!is_array($oauthClient) && !$isServiceAccount) {
        throw new RuntimeException('GOOGLE_DRIVE_CREDENTIALS_JSON không đúng định dạng Service Account hoặc OAuth Client.');
    }
    return $credentials;
}

function drive_http(string $method, string $url, array $headers = [], ?string $body = null): array
{
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_CONNECTTIMEOUT => 15,
            CURLOPT_TIMEOUT => 120,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_HEADER => true,
        ]);
        if ($body !== null) curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        $raw = curl_exec($ch);
        if ($raw === false) {
            $message = curl_error($ch);
            curl_close($ch);
            throw new RuntimeException('Không kết nối được Google Drive: ' . $message);
        }
        $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $headerSize = (int)curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $responseBody = substr($raw, $headerSize);
        curl_close($ch);
    } else {
        $context = stream_context_create(['http' => [
            'method' => $method,
            'header' => implode("\r\n", $headers),
            'content' => $body ?? '',
            'ignore_errors' => true,
            'timeout' => 120,
        ]]);
        $responseBody = @file_get_contents($url, false, $context);
        if ($responseBody === false) {
            throw new RuntimeException('Hosting không thể kết nối đến Google Drive.');
        }
        $status = 0;
        foreach ($http_response_header ?? [] as $line) {
            if (preg_match('/^HTTP\/\S+\s+(\d+)/', $line, $match)) $status = (int)$match[1];
        }
    }

    if ($status < 200 || $status >= 300) {
        $decoded = json_decode((string)$responseBody, true);
        $detail = $decoded['error']['message'] ?? $decoded['error_description'] ?? ('HTTP ' . $status);
        throw new RuntimeException('Google Drive từ chối yêu cầu: ' . $detail);
    }

    $decoded = json_decode((string)$responseBody, true);
    return is_array($decoded) ? $decoded : ['raw' => (string)$responseBody];
}

function drive_access_token(): string
{
    static $cachedToken = null;
    static $expiresAt = 0;
    if ($cachedToken && $expiresAt > time() + 60) return $cachedToken;

    $credentials = drive_credentials();
    $now = time();
    $oauthClient = $credentials['installed'] ?? $credentials['web'] ?? null;
    if (is_array($oauthClient)) {
        $tokenRaw = defined('GOOGLE_DRIVE_TOKEN_JSON') ? trim((string)GOOGLE_DRIVE_TOKEN_JSON) : '';
        $tokenData = json_decode($tokenRaw, true);
        if (!is_array($tokenData) || empty($tokenData['refresh_token'])) {
            throw new RuntimeException('Cấu hình OAuth cần GOOGLE_DRIVE_TOKEN_JSON có refresh_token.');
        }
        $body = http_build_query([
            'client_id' => $oauthClient['client_id'] ?? '',
            'client_secret' => $oauthClient['client_secret'] ?? '',
            'refresh_token' => $tokenData['refresh_token'],
            'grant_type' => 'refresh_token',
        ]);
        $response = drive_http('POST', $oauthClient['token_uri'] ?? 'https://oauth2.googleapis.com/token', [
            'Content-Type: application/x-www-form-urlencoded',
            'Content-Length: ' . strlen($body),
        ], $body);
        if (empty($response['access_token'])) throw new RuntimeException('Google không trả về OAuth access token.');
        $cachedToken = (string)$response['access_token'];
        $expiresAt = $now + (int)($response['expires_in'] ?? 3600);
        return $cachedToken;
    }

    $header = drive_base64url(json_encode(['alg' => 'RS256', 'typ' => 'JWT']));
    $claims = drive_base64url(json_encode([
        'iss' => $credentials['client_email'],
        'scope' => 'https://www.googleapis.com/auth/drive',
        'aud' => 'https://oauth2.googleapis.com/token',
        'iat' => $now,
        'exp' => $now + 3600,
    ]));
    $signingInput = $header . '.' . $claims;
    $privateKey = str_replace('\\n', "\n", (string)$credentials['private_key']);
    $signature = '';
    if (!function_exists('openssl_sign') || !openssl_sign($signingInput, $signature, $privateKey, OPENSSL_ALGO_SHA256)) {
        throw new RuntimeException('Hosting cần bật extension OpenSSL để kết nối Google Drive.');
    }

    $assertion = $signingInput . '.' . drive_base64url($signature);
    $body = http_build_query([
        'grant_type' => 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion' => $assertion,
    ]);
    $response = drive_http('POST', 'https://oauth2.googleapis.com/token', [
        'Content-Type: application/x-www-form-urlencoded',
        'Content-Length: ' . strlen($body),
    ], $body);
    if (empty($response['access_token'])) {
        throw new RuntimeException('Google không trả về access token.');
    }
    $cachedToken = (string)$response['access_token'];
    $expiresAt = $now + (int)($response['expires_in'] ?? 3600);
    return $cachedToken;
}

function drive_api(string $method, string $url, ?array $json = null): array
{
    $headers = ['Authorization: Bearer ' . drive_access_token()];
    $body = null;
    if ($json !== null) {
        $body = json_encode($json, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $headers[] = 'Content-Type: application/json; charset=utf-8';
        $headers[] = 'Content-Length: ' . strlen($body);
    }
    return drive_http($method, $url, $headers, $body);
}

function drive_safe_name(string $name, string $fallback = 'tep'): string
{
    $name = trim(preg_replace('/[\\\\\/:*?"<>|\x00-\x1F]+/u', '-', $name));
    $name = preg_replace('/\s+/u', ' ', $name);
    if ($name === '' || $name === '.' || $name === '..') $name = $fallback;
    return function_exists('mb_substr') ? mb_substr($name, 0, 180) : substr($name, 0, 180);
}

function drive_escape_query(string $value): string
{
    return str_replace(['\\', "'"], ['\\\\', "\\'"], $value);
}

function drive_find_folder(string $parentId, string $name): ?string
{
    $query = "mimeType='application/vnd.google-apps.folder' and trashed=false and '" .
        drive_escape_query($parentId) . "' in parents and name='" . drive_escape_query($name) . "'";
    $url = 'https://www.googleapis.com/drive/v3/files?' . http_build_query([
        'q' => $query,
        'spaces' => 'drive',
        'fields' => 'files(id,name)',
        'pageSize' => 1,
        'supportsAllDrives' => 'true',
        'includeItemsFromAllDrives' => 'true',
    ]);
    $response = drive_api('GET', $url);
    return !empty($response['files'][0]['id']) ? (string)$response['files'][0]['id'] : null;
}

function drive_create_folder(string $parentId, string $name): string
{
    $response = drive_api('POST', 'https://www.googleapis.com/drive/v3/files?supportsAllDrives=true&fields=id', [
        'name' => drive_safe_name($name, 'Thu muc'),
        'mimeType' => 'application/vnd.google-apps.folder',
        'parents' => [$parentId],
    ]);
    if (empty($response['id'])) throw new RuntimeException('Không tạo được thư mục trên Google Drive.');
    return (string)$response['id'];
}

function drive_get_or_create_folder(string $parentId, string $name): string
{
    $safeName = drive_safe_name($name, 'Thu muc');
    return drive_find_folder($parentId, $safeName) ?: drive_create_folder($parentId, $safeName);
}

function drive_school_year(?string $value = null): string
{
    $value = trim((string)$value);
    if (preg_match('/^\d{4}\s*-\s*\d{4}$/', $value)) return str_replace(' ', '', $value);
    $year = (int)date('Y');
    $month = (int)date('n');
    return $month >= 8 ? ($year . '-' . ($year + 1)) : (($year - 1) . '-' . $year);
}

function drive_assignment_folder(string $title, string $submissionType = 'file', ?string $academicYear = null): string
{
    $root = defined('GOOGLE_DRIVE_ROOT_FOLDER_ID') ? trim((string)GOOGLE_DRIVE_ROOT_FOLDER_ID) : '';
    if ($root === '') throw new RuntimeException('Chưa cấu hình GOOGLE_DRIVE_ROOT_FOLDER_ID trên hosting.');
    $category = $submissionType === 'report' ? '01_BAO_CAO' : '02_NOP_BAI';
    $categoryFolder = drive_get_or_create_folder($root, $category);
    $yearFolder = drive_get_or_create_folder($categoryFolder, 'NAM_HOC_' . drive_school_year($academicYear));
    return drive_create_folder($yearFolder, drive_safe_name($title, 'Dot nop'));
}

function drive_submission_stored_name(string $groupName, string $fullName, string $identifier, int $index, string $originalName, ?string $fieldKey = null): string
{
    $parts = [];
    if (trim($groupName) !== '') $parts[] = drive_safe_name($groupName, 'Lop');
    $parts[] = drive_safe_name(trim($fullName) !== '' ? $fullName : 'Nguoi nop', 'Nguoi nop');
    if (trim($identifier) !== '') $parts[] = drive_safe_name($identifier, 'Ma');
    if ($fieldKey) $parts[] = drive_safe_name($fieldKey, 'Minh chung');
    $parts[] = date('Ymd-His') . '-' . $index;
    $parts[] = drive_safe_name($originalName, 'tep');
    $name = implode(' - ', $parts);
    return function_exists('mb_substr') ? mb_substr($name, 0, 180) : substr($name, 0, 180);
}

function drive_participant_folder(string $assignmentFolderId, string $groupName, string $fullName, string $identifier): string
{
    $groupFolder = drive_get_or_create_folder($assignmentFolderId, trim($groupName) !== '' ? $groupName : 'CHUA_PHAN_NHOM');
    return drive_get_or_create_folder($groupFolder, trim($fullName) . ' - ' . trim($identifier));
}

function drive_lotrinh_self_practice_folder(string $subject, string $lessonTitle, int $lessonId): string
{
    $root = defined('GOOGLE_DRIVE_ROOT_FOLDER_ID') ? trim((string)GOOGLE_DRIVE_ROOT_FOLDER_ID) : '';
    if ($root === '') {
        throw new RuntimeException('Chưa cấu hình GOOGLE_DRIVE_ROOT_FOLDER_ID trên hosting.');
    }
    $categoryFolder = drive_get_or_create_folder($root, '04_LO_TRINH_TU_LUYEN');
    $yearFolder = drive_get_or_create_folder($categoryFolder, 'NAM_HOC_' . drive_school_year());
    $subjectFolder = drive_get_or_create_folder($yearFolder, drive_safe_name($subject, 'Mon hoc'));
    return drive_get_or_create_folder($subjectFolder, drive_safe_name('[' . $lessonId . '] ' . $lessonTitle, 'Bai hoc'));
}

function drive_board_folder(string $publicCode, string $title, ?string $academicYear = null): string
{
    $root = defined('GOOGLE_DRIVE_ROOT_FOLDER_ID') ? trim((string)GOOGLE_DRIVE_ROOT_FOLDER_ID) : '';
    if ($root === '') throw new RuntimeException('Chưa cấu hình GOOGLE_DRIVE_ROOT_FOLDER_ID trên hosting.');
    $categoryFolder = drive_get_or_create_folder($root, '03_BANG_CHIA_SE');
    $yearFolder = drive_get_or_create_folder($categoryFolder, 'NAM_HOC_' . drive_school_year($academicYear));
    return drive_get_or_create_folder($yearFolder, '[' . $publicCode . '] ' . $title);
}

function drive_file_header(string $tmpPath, int $length = 16): string
{
    $head = file_get_contents($tmpPath, false, null, 0, $length);
    return $head === false ? '' : $head;
}

function drive_office_mimes(): array
{
    return [
        'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx' => 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'pptx' => 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'doc' => 'application/msword',
        'xls' => 'application/vnd.ms-excel',
        'ppt' => 'application/vnd.ms-powerpoint',
        'odt' => 'application/vnd.oasis.opendocument.text',
        'ods' => 'application/vnd.oasis.opendocument.spreadsheet',
        'odp' => 'application/vnd.oasis.opendocument.presentation',
        'pdf' => 'application/pdf',
        'rtf' => 'application/rtf',
    ];
}

function drive_detect_mime(string $tmpPath, string $originalName, string $browserMime = ''): string
{
    $ext = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
    $office = drive_office_mimes();
    $detected = '';
    if (function_exists('finfo_open')) {
        $detected = (string)(new finfo(FILEINFO_MIME_TYPE))->file($tmpPath);
    }
    if ($detected === '' && $browserMime !== '') $detected = $browserMime;

    $head = drive_file_header($tmpPath, 4);
    if (isset($office[$ext])) {
        if (in_array($ext, ['docx', 'xlsx', 'pptx', 'odt', 'ods', 'odp'], true) && str_starts_with($head, "PK\x03\x04")) {
            return $office[$ext];
        }
        if ($ext === 'doc' && str_starts_with($head, "\xD0\xCF\x11\xE0")) return $office[$ext];
        if ($ext === 'pdf' && str_starts_with($head, '%PDF')) return $office['pdf'];
        if ($detected !== '' && !in_array($detected, ['application/octet-stream', 'application/zip', 'text/plain'], true)) {
            return $detected;
        }
        return $office[$ext];
    }
    return $detected !== '' ? $detected : ($browserMime !== '' ? $browserMime : 'application/octet-stream');
}

function drive_validate_upload(string $tmpPath, string $originalName): ?string
{
    $ext = strtolower(pathinfo($originalName, PATHINFO_EXTENSION));
    $head = drive_file_header($tmpPath, 48);
    if ($head === '') return 'Không đọc được nội dung tệp.';

    if (in_array($ext, ['docx', 'xlsx', 'pptx'], true)) {
        if (str_starts_with($head, "PK\x03\x04")) return null;
        if (str_starts_with($head, 'MIME-Version:') || str_contains($head, 'Content-Transfer-Encoding: base64')) {
            return 'Tệp .' . $ext . ' không hợp lệ — đây là trang web/mã HTML được lưu nhầm thành Word. Hãy mở bằng Microsoft Word hoặc Word Online, chọn Lưu thành .' . $ext . ' thật, hoặc xuất sang PDF rồi đăng lại.';
        }
        return 'Tệp .' . $ext . ' bị lỗi hoặc không đúng định dạng Office. Hãy mở và Lưu lại bằng Word/Excel, hoặc đăng bản PDF.';
    }
    return null;
}

function drive_google_convert_mime(string $ext, string $tmpPath): ?string
{
    $ext = strtolower($ext);
    $head = drive_file_header($tmpPath, 4);
    $map = [
        'docx' => 'application/vnd.google-apps.document',
        'doc' => 'application/vnd.google-apps.document',
        'odt' => 'application/vnd.google-apps.document',
        'rtf' => 'application/vnd.google-apps.document',
        'xlsx' => 'application/vnd.google-apps.spreadsheet',
        'xls' => 'application/vnd.google-apps.spreadsheet',
        'ods' => 'application/vnd.google-apps.spreadsheet',
        'pptx' => 'application/vnd.google-apps.presentation',
        'ppt' => 'application/vnd.google-apps.presentation',
        'odp' => 'application/vnd.google-apps.presentation',
    ];
    if (!isset($map[$ext])) return null;
    if (in_array($ext, ['docx', 'xlsx', 'pptx', 'odt', 'ods', 'odp'], true) && !str_starts_with($head, "PK\x03\x04")) return null;
    if ($ext === 'doc' && !str_starts_with($head, "\xD0\xCF\x11\xE0")) return null;
    return $map[$ext];
}

function drive_upload_file(string $folderId, string $storedName, string $mimeType, string $tmpPath, bool $convertToGoogle = true): array
{
    $content = file_get_contents($tmpPath);
    if ($content === false) throw new RuntimeException('Không đọc được tệp tạm để tải lên Drive.');

    $ext = strtolower(pathinfo($storedName, PATHINFO_EXTENSION));
    $mediaMime = $mimeType !== '' ? $mimeType : 'application/octet-stream';
    $metadata = [
        'name' => drive_safe_name($storedName),
        'parents' => [$folderId],
    ];
    $googleMime = $convertToGoogle ? drive_google_convert_mime($ext, $tmpPath) : null;
    if ($googleMime) $metadata['mimeType'] = $googleMime;

    if ($googleMime) {
        $boundary = 'giangbai_' . bin2hex(random_bytes(12));
        $metaJson = json_encode($metadata, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $body = '--' . $boundary . "\r\n" .
            "Content-Type: application/json; charset=UTF-8\r\n\r\n" .
            $metaJson . "\r\n" .
            '--' . $boundary . "\r\n" .
            'Content-Type: ' . $mediaMime . "\r\n" .
            "Content-Transfer-Encoding: binary\r\n\r\n" .
            $content . "\r\n" .
            '--' . $boundary . '--';
        $response = drive_http(
            'POST',
            'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&fields=id,name,webViewLink,webContentLink,mimeType',
            [
                'Authorization: Bearer ' . drive_access_token(),
                'Content-Type: multipart/related; boundary=' . $boundary,
                'Content-Length: ' . strlen($body),
            ],
            $body
        );
    } else {
        $response = drive_http(
            'POST',
            'https://www.googleapis.com/upload/drive/v3/files?uploadType=media&supportsAllDrives=true&fields=id,name,webViewLink,webContentLink,mimeType',
            [
                'Authorization: Bearer ' . drive_access_token(),
                'Content-Type: ' . $mediaMime,
                'Content-Length: ' . strlen($content),
            ],
            $content
        );
        if (empty($response['id'])) throw new RuntimeException('Google Drive không trả về mã tệp.');
        $fileId = (string)$response['id'];
        $response = drive_api(
            'PATCH',
            'https://www.googleapis.com/drive/v3/files/' . rawurlencode($fileId) .
                '?addParents=' . rawurlencode($folderId) .
                '&supportsAllDrives=true&fields=id,name,webViewLink,webContentLink,mimeType',
            ['name' => $metadata['name']]
        );
    }

    if (empty($response['id'])) throw new RuntimeException('Google Drive không trả về mã tệp.');
    $fileId = (string)$response['id'];

    if (defined('GOOGLE_DRIVE_SHARE_MODE') && GOOGLE_DRIVE_SHARE_MODE === 'anyone') {
        drive_api('POST', 'https://www.googleapis.com/drive/v3/files/' . rawurlencode($fileId) . '/permissions?supportsAllDrives=true', [
            'type' => 'anyone',
            'role' => 'reader',
        ]);
    }

    return [
        'file_id' => $fileId,
        'stored_name' => (string)($response['name'] ?? $storedName),
        'mime_type' => (string)($response['mimeType'] ?? $mediaMime),
        'view_url' => (string)($response['webViewLink'] ?? ('https://drive.google.com/file/d/' . $fileId . '/view')),
        'download_url' => (string)($response['webContentLink'] ?? ('https://drive.google.com/uc?export=download&id=' . $fileId)),
    ];
}

function drive_delete_file(string $fileId): void
{
    $fileId = trim($fileId);
    if ($fileId === '') return;
    try {
        drive_api('DELETE', 'https://www.googleapis.com/drive/v3/files/' . rawurlencode($fileId) . '?supportsAllDrives=true');
    } catch (RuntimeException $e) {
        $message = $e->getMessage();
        if (str_contains($message, 'File not found') || str_contains($message, 'HTTP 404')) return;
        throw $e;
    }
}

function drive_download_file(string $fileId): string
{
    $url = 'https://www.googleapis.com/drive/v3/files/' . rawurlencode($fileId) . '?alt=media&supportsAllDrives=true';
    $headers = ['Authorization: Bearer ' . drive_access_token()];
    if (function_exists('curl_init')) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_CONNECTTIMEOUT => 15,
            CURLOPT_TIMEOUT => 300,
            CURLOPT_HTTPHEADER => $headers,
        ]);
        $body = curl_exec($ch);
        $status = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        if ($body === false || $status < 200 || $status >= 300) {
            throw new RuntimeException('Không tải được tệp từ Google Drive' . ($error ? ': ' . $error : '.'));
        }
        return $body;
    }
    $context = stream_context_create(['http' => ['header' => implode("\r\n", $headers), 'timeout' => 300, 'ignore_errors' => true]]);
    $body = @file_get_contents($url, false, $context);
    if ($body === false) throw new RuntimeException('Hosting không thể tải tệp từ Google Drive.');
    return $body;
}
