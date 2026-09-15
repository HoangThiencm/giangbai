<?php
/** Proxy Gemini dành riêng cho Canvas: key luôn chỉ được dùng ở máy chủ. */
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/ai_runtime_config.php';
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-User-Account');
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') { http_response_code(204); exit; }
function canvas_user_account(array $body = []): string {$value=$body['user_account']??($_GET['user_account']??($_SERVER['HTTP_X_USER_ACCOUNT']??''));return trim(rawurldecode((string)$value));}
function canvas_user_keys(string $account): array {
    global $pdo;
    if ($account === '' || !isset($pdo) || !$pdo instanceof PDO) return [[], [], 'Không thể kết nối khoá cá nhân.'];
    $prefix = strstr($account, '@', true) ?: $account;
    try {
        // Tài khoản Canvas có thể được nhập dưới dạng username hoặc username@example.com.
        // Chỉ dùng username như luồng user_phuluc_draft để không phụ thuộc cột email ở production.
        $stmt = $pdo->prepare('SELECT username, gemini_keys FROM users WHERE (username = ? OR username = ?) AND is_active = 1 LIMIT 1');
        $stmt->execute([$account, $prefix]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC) ?: [];
        return [$row, parse_stored_api_keys($row['gemini_keys'] ?? null), ''];
    } catch (Throwable $e) {
        error_log('Canvas Gemini key lookup failed: ' . $e->getMessage());
        return [[], [], 'Không thể đồng bộ API Key lúc này.'];
    }
}
function canvas_gemini_call(string $model,string $key,string $encoded,int $timeout): array {$url='https://generativelanguage.googleapis.com/v1beta/models/'.rawurlencode($model).':generateContent?key='.rawurlencode($key);$ch=curl_init($url);curl_setopt_array($ch,[CURLOPT_RETURNTRANSFER=>true,CURLOPT_POST=>true,CURLOPT_HTTPHEADER=>['Content-Type: application/json'],CURLOPT_POSTFIELDS=>$encoded,CURLOPT_CONNECTTIMEOUT=>10,CURLOPT_TIMEOUT=>$timeout]);$raw=curl_exec($ch);$status=(int)curl_getinfo($ch,CURLINFO_HTTP_CODE);$curlError=curl_error($ch);curl_close($ch);$decoded=is_string($raw)&&$raw!==''?json_decode($raw,true):null;$error=is_array($decoded)?(string)($decoded['error']['message']??('Gemini HTTP '.$status)):($curlError!==''?'Máy chủ không gọi được Gemini: '.$curlError:'Gemini trả về dữ liệu không hợp lệ.');return ['ok'=>is_array($decoded)&&$status>=200&&$status<300,'body'=>$decoded,'status'=>$status?:502,'error'=>$error];}
function canvas_is_quota_failure(array $attempt): bool { return $attempt['status'] === 429 || (bool)preg_match('/quota|resource exhausted|rate limit/i', (string)$attempt['error']); }
function canvas_is_timeout_or_transient_failure(array $attempt): bool { return in_array((int)$attempt['status'], [0, 408, 425, 500, 502, 503, 504], true) || (bool)preg_match('/timed? out|timeout|couldn.t connect|could not resolve|network|connection|temporar|unavailable/i', (string)$attempt['error']); }
$method=$_SERVER['REQUEST_METHOD']??'';$body=$method==='POST'?json_body():[];$account=canvas_user_account($body);$action=trim((string)($body['action']??($_GET['action']??'')));
if($action==='key_status'){[$user,$userKeys,$keyError]=canvas_user_keys($account);if($keyError!=='')respond(['ok'=>false,'error'=>$keyError,'user_account'=>$account,'key_count'=>0,'gemini_key_count'=>0,'masked_keys'=>[]],503);respond(['ok'=>true,'user_account'=>$account,'key_count'=>count($userKeys),'gemini_key_count'=>count($userKeys),'masked_keys'=>array_values(array_filter(array_map('mask_user_api_key',$userKeys))),'has_user_keys'=>!empty($userKeys)]);}
if($method!=='POST')respond(['ok'=>false,'error'=>'Method not allowed.'],405);
$payload=$body['payload']??null;if(!is_array($payload)||empty($payload['contents']))respond(['ok'=>false,'error'=>'Thiếu nội dung gửi Gemini.'],422);$encoded=json_encode($payload,JSON_UNESCAPED_UNICODE);if(!is_string($encoded)||strlen($encoded)>8*1024*1024)respond(['ok'=>false,'error'=>'Tài liệu quá lớn để Canvas gửi tới Gemini.'],413);
$runtime=load_ai_runtime_config();$systemKeys=$runtime['gemini_keys']??[];$systemAvailable=!empty($runtime['gemini_enabled'])&&!empty($systemKeys);$timeout=max(10,min(90,(int)($body['timeout']??75)));$deadline=microtime(true)+$timeout;$tier=($body['tier']??'')==='high_reasoning'?'high_reasoning':'heavy_io';$preferredModel=trim((string)($body['preferred_model']??'gemini-3.8-flash'));if(!preg_match('/^gemini-[a-z0-9._-]+$/i',$preferredModel))$preferredModel='gemini-3.8-flash';[$user,$userKeys]=canvas_user_keys($account);if(!$userKeys&&!$systemAvailable)respond(['ok'=>false,'error'=>'Gemini Canvas chưa có API Key cá nhân hợp lệ và Admin chưa cấu hình khóa hệ thống.','fallback_attempted'=>false,'fallback_outcome'=>'system_unavailable','system_key_available'=>false],503);$last=['status'=>502,'error'=>'Không gọi được Gemini Canvas.'];$quotaKeyIndexes=[];$fallbackReason=$userKeys?'':'no_user_key';
// Reserve most of the request budget for the system fallback. Only quota failures rotate user keys.
$userAttemptTimeout=min(25,max(10,$timeout-35));
if($userKeys)foreach($userKeys as $index=>$key){$attempt=canvas_gemini_call($preferredModel,$key,$encoded,$userAttemptTimeout);if($attempt['ok'])respond(['ok'=>true,'body'=>$attempt['body'],'model'=>$preferredModel,'tier'=>'user_key','key_index'=>$index+1,'total_user_keys'=>count($userKeys),'rotation_count'=>count($quotaKeyIndexes),'quota_key_indexes'=>$quotaKeyIndexes,'fallback_used'=>false,'fallback_attempted'=>false,'fallback_outcome'=>'not_needed','system_key_available'=>$systemAvailable]);$last=$attempt;if(canvas_is_quota_failure($attempt)){$quotaKeyIndexes[]=$index+1;$fallbackReason='user_key_quota';continue;}$fallbackReason=canvas_is_timeout_or_transient_failure($attempt)?'user_key_timeout':'user_key_error';break;}
if($systemAvailable)foreach($systemKeys as $key){$remaining=(int)floor($deadline-microtime(true)-3);if($remaining<10)break;$systemAttemptTimeout=min(55,$remaining);$attempt=canvas_gemini_call('gemini-3-flash-preview',$key,$encoded,$systemAttemptTimeout);if($attempt['ok'])respond(['ok'=>true,'body'=>$attempt['body'],'model'=>'gemini-3-flash-preview','tier'=>$userKeys?'fallback_system':'system_key','fallback_used'=>!empty($userKeys),'fallback_reason'=>$userKeys?$fallbackReason:null,'fallback_attempted'=>!empty($userKeys),'fallback_outcome'=>$userKeys?'success':'not_needed','system_key_available'=>true,'total_user_keys'=>count($userKeys),'rotation_count'=>count($quotaKeyIndexes),'quota_key_indexes'=>$quotaKeyIndexes]);$last=$attempt;}
$fallbackAttempted=!empty($userKeys);$fallbackOutcome=$fallbackAttempted?($systemAvailable?'failed':'system_unavailable'):'system_failed';$message=$fallbackOutcome==='system_unavailable'?'Key cá nhân không gọi được và Gemini nội bộ chưa được Admin cấu hình.':$last['error'];respond(['ok'=>false,'error'=>$message,'fallback_attempted'=>$fallbackAttempted,'fallback_outcome'=>$fallbackOutcome,'fallback_reason'=>$fallbackAttempted?$fallbackReason:null,'system_key_available'=>$systemAvailable,'total_user_keys'=>count($userKeys),'rotation_count'=>count($quotaKeyIndexes),'quota_key_indexes'=>$quotaKeyIndexes],$last['status']>=400&&$last['status']<500?$last['status']:502);
