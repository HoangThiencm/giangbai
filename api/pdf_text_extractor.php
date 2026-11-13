<?php
/**
 * Trích xuất chữ từ PDF có lớp text, chỉ dùng zlib của PHP.
 * Đủ cho header văn bản hành chính: FlateDecode, ToUnicode CMap, Identity-H, WinAnsi.
 */
function vbd_pdf_extract_text(string $pdfPath, int $maxPages = 3): string
{
    if ($maxPages < 1) $maxPages = 1;
    if (!is_file($pdfPath)) return '';
    $data = @file_get_contents($pdfPath);
    if (!is_string($data) || strncmp($data, '%PDF', 4) !== 0) return '';
    $deadline = microtime(true) + 3.0;
    $objects = vbd_pdf_index_objects($data);
    if (!$objects) return '';
    vbd_pdf_expand_object_streams($objects, $deadline);
    $pages = vbd_pdf_page_ids($objects, $maxPages);
    $chunks = [];
    foreach ($pages as $pageIndex => $pageId) {
        if (microtime(true) > $deadline) break;
        $text = vbd_pdf_page_text($objects, $pageId, $pageIndex + 1);
        if ($text !== '') $chunks[] = $text;
    }
    $text = vbd_pdf_clean_text(implode("\n", $chunks));
    $signature = vbd_pdf_signature_hint($data);
    if ($signature !== '') $text = $signature . "\n" . $text;
    return trim($text);
}

function vbd_pdf_signature_hint(string $data): string
{
    if (!preg_match_all('/\/M\s*\(\s*D:(\d{4})(\d{2})(\d{2})/', $data, $matches, PREG_SET_ORDER)) return '';
    $best = '';
    foreach ($matches as $match) {
        $stamp = $match[1] . $match[2] . $match[3];
        if ($stamp > $best) $best = $stamp;
    }
    return $best === '' ? '' : '/M(D:' . $best . ')';
}

function vbd_pdf_index_objects(string $data): array
{
    $objects = [];
    $length = strlen($data);
    if (!preg_match_all('/(\d+)\s+\d+\s+obj\b/', $data, $matches, PREG_OFFSET_CAPTURE)) return [];
    foreach ($matches[0] as $index => $hit) {
        $id = (int)$matches[1][$index][0];
        $start = $hit[1] + strlen($hit[0]);
        $endObj = strpos($data, 'endobj', $start);
        if ($endObj === false) continue;
        $streamAt = strpos($data, 'stream', $start);
        if ($streamAt !== false && $streamAt < $endObj) {
            $endStream = strpos($data, 'endstream', $streamAt + 6);
            if ($endStream === false) continue;
            $endObj = strpos($data, 'endobj', $endStream);
            if ($endObj === false) continue;
        }
        $objects[$id] = substr($data, $start, $endObj - $start);
    }
    return $objects;
}

function vbd_pdf_dict(string $body): string
{
    $start = strpos($body, '<<');
    if ($start === false) return '';
    $length = strlen($body);
    $depth = 0;
    for ($i = $start; $i < $length - 1; $i++) {
        if ($body[$i] === '<' && $body[$i + 1] === '<') {
            $depth++;
            $i++;
            continue;
        }
        if ($body[$i] === '>' && $body[$i + 1] === '>') {
            $depth--;
            $i++;
            if ($depth === 0) return substr($body, $start, $i + 1 - $start);
        }
    }
    return '';
}

function vbd_pdf_dict_int(string $dict, string $key): int
{
    if (preg_match('#/' . preg_quote($key, '#') . '\s+(-?\d+)#', $dict, $match)) return (int)$match[1];
    return 0;
}

function vbd_pdf_inner_dict(string $dict, string $key): string
{
    if (!preg_match('#/' . preg_quote($key, '#') . '\s*<<#', $dict, $match, PREG_OFFSET_CAPTURE)) return '';
    $start = $match[0][1] + strlen($match[0][0]) - 2;
    return vbd_pdf_dict(substr($dict, $start));
}

function vbd_pdf_stream(string $body, ?string $dict = null): string
{
    $dict ??= vbd_pdf_dict($body);
    if (preg_match('#/Subtype\s*/Image\b#', $dict)) return '';
    $marker = strpos($body, 'stream');
    if ($marker === false) return '';
    $start = $marker + 6;
    if (substr($body, $start, 2) === "\r\n") $start += 2;
    elseif (isset($body[$start]) && ($body[$start] === "\n" || $body[$start] === "\r")) $start += 1;
    $end = strrpos($body, 'endstream');
    if ($end === false || $end < $start) return '';
    $blob = substr($body, $start, $end - $start);
    if (str_ends_with($blob, "\r\n")) $blob = substr($blob, 0, -2);
    elseif (str_ends_with($blob, "\n") || str_ends_with($blob, "\r")) $blob = substr($blob, 0, -1);
    if (!preg_match('#/FlateDecode\b#', $dict)) return $blob;
    $decoded = @gzuncompress($blob);
    if (!is_string($decoded)) $decoded = @gzinflate($blob);
    if (!is_string($decoded) && strlen($blob) > 2) $decoded = @gzinflate(substr($blob, 2));
    return is_string($decoded) ? $decoded : '';
}

function vbd_pdf_expand_object_streams(array &$objects, float $deadline): void
{
    $extra = [];
    foreach ($objects as $body) {
        if (microtime(true) > $deadline) break;
        $dict = vbd_pdf_dict($body);
        if (!preg_match('#/Type\s*/ObjStm\b#', $dict)) continue;
        $stream = vbd_pdf_stream($body, $dict);
        if ($stream === '') continue;
        $count = vbd_pdf_dict_int($dict, 'N');
        $first = vbd_pdf_dict_int($dict, 'First');
        if ($count < 1 || $first < 1 || $first >= strlen($stream)) continue;
        if (!preg_match_all('/(\d+)\s+(\d+)/', substr($stream, 0, $first), $pairs)) continue;
        $pairsCount = min($count, count($pairs[1]));
        for ($i = 0; $i < $pairsCount; $i++) {
            $objectId = (int)$pairs[1][$i];
            if (isset($objects[$objectId]) || isset($extra[$objectId])) continue;
            $offset = $first + (int)$pairs[2][$i];
            $next = ($i + 1 < $pairsCount) ? $first + (int)$pairs[2][$i + 1] : strlen($stream);
            if ($offset < 0 || $next <= $offset || $offset > strlen($stream)) continue;
            $extra[$objectId] = substr($stream, $offset, $next - $offset);
        }
    }
    foreach ($extra as $objectId => $body) $objects[$objectId] = $body;
}

function vbd_pdf_page_ids(array $objects, int $maxPages): array
{
    $root = 0;
    foreach ($objects as $body) {
        $dict = vbd_pdf_dict($body);
        if (!preg_match('#/Type\s*/Catalog\b#', $dict)) continue;
        if (preg_match('#/Pages\s+(\d+)\s+0\s+R#', $dict, $match)) $root = (int)$match[1];
        break;
    }
    $pages = [];
    $seen = [];
    $walk = function (int $id) use (&$walk, &$pages, &$seen, $objects, $maxPages): void {
        if ($id < 1 || isset($seen[$id]) || !isset($objects[$id]) || count($pages) >= $maxPages) return;
        $seen[$id] = true;
        $dict = vbd_pdf_dict($objects[$id]);
        if (preg_match('#/Type\s*/Pages\b#', $dict)) {
            if (preg_match('#/Kids\s*\[(.*?)\]#s', $dict, $kids) && preg_match_all('#(\d+)\s+0\s+R#', $kids[1], $refs)) {
                foreach ($refs[1] as $ref) $walk((int)$ref);
            }
            return;
        }
        if (preg_match('#/Type\s*/Page\b#', $dict)) $pages[] = $id;
    };
    if ($root) $walk($root);
    if ($pages) return $pages;
    foreach ($objects as $id => $body) {
        if (count($pages) >= $maxPages) break;
        $dict = vbd_pdf_dict($body);
        if (preg_match('#/Type\s*/Page\b#', $dict) && !preg_match('#/Type\s*/Pages\b#', $dict)) $pages[] = (int)$id;
    }
    return $pages;
}

function vbd_pdf_font_maps(array $objects, string $pageDict, int $depth = 0): array
{
    if ($depth > 6) return [];
    $resourceDict = $pageDict;
    if (preg_match('#/Resources\s+(\d+)\s+0\s+R#', $pageDict, $match) && isset($objects[(int)$match[1]])) {
        $resourceDict = vbd_pdf_dict($objects[(int)$match[1]]);
    }
    $fontDict = vbd_pdf_inner_dict($resourceDict, 'Font');
    if ($fontDict === '' && preg_match('#/Parent\s+(\d+)\s+0\s+R#', $pageDict, $parent) && isset($objects[(int)$parent[1]])) {
        return vbd_pdf_font_maps($objects, vbd_pdf_dict($objects[(int)$parent[1]]), $depth + 1);
    }
    $fonts = [];
    if ($fontDict !== '' && preg_match_all('#/([A-Za-z][A-Za-z0-9]*)\s+(\d+)\s+0\s+R#', $fontDict, $refs, PREG_SET_ORDER)) {
        foreach ($refs as $ref) $fonts[$ref[1]] = vbd_pdf_font_info($objects, (int)$ref[2]);
    }
    return $fonts;
}

function vbd_pdf_font_info(array $objects, int $id): array
{
    $info = ['enc' => 'utf8', 'cmap' => null];
    if (!isset($objects[$id])) return $info;
    $dict = vbd_pdf_dict($objects[$id]);
    if (preg_match('#/Encoding\s*/WinAnsiEncoding\b#', $dict)) $info['enc'] = 'winansi';
    if (preg_match('#/Identity-H\b#', $dict)) $info['enc'] = 'identity';
    if (preg_match('#/ToUnicode\s+(\d+)\s+0\s+R#', $dict, $match) && isset($objects[(int)$match[1]])) {
        $stream = vbd_pdf_stream($objects[(int)$match[1]]);
        if ($stream !== '') {
            $info['cmap'] = vbd_pdf_cmap($stream);
            $info['enc'] = 'identity';
        }
    }
    return $info;
}

function vbd_pdf_cmap(string $text): array
{
    $bf = [];
    $ranges = [];
    $width = 4;
    if (preg_match('/begincodespacerange\s*<\s*([0-9A-Fa-f]+)\s*>/', $text, $match)) {
        $width = strlen($match[1]);
        if ($width % 2) $width++;
        if ($width < 2) $width = 2;
    }
    if (preg_match_all('/beginbfchar(.*?)endbfchar/s', $text, $blocks)) {
        foreach ($blocks[1] as $block) {
            if (!preg_match_all('/<\s*([0-9A-Fa-f]+)\s*>\s*<\s*([0-9A-Fa-f\s]+)\s*>/', $block, $pairs, PREG_SET_ORDER)) continue;
            foreach ($pairs as $pair) $bf[hexdec($pair[1])] = vbd_pdf_hex_to_utf8($pair[2]);
        }
    }
    if (preg_match_all('/beginbfrange(.*?)endbfrange/s', $text, $blocks)) {
        foreach ($blocks[1] as $block) {
            if (preg_match_all('/<\s*([0-9A-Fa-f]+)\s*>\s*<\s*([0-9A-Fa-f]+)\s*>\s*\[([^\]]*)\]/', $block, $rows, PREG_SET_ORDER)) {
                foreach ($rows as $row) {
                    preg_match_all('/<\s*([0-9A-Fa-f\s]+)\s*>/', $row[3], $dests);
                    $chars = [];
                    foreach ($dests[1] as $hex) $chars[] = vbd_pdf_hex_to_utf8($hex);
                    $ranges[] = [hexdec($row[1]), hexdec($row[2]), $chars];
                }
            }
            $plain = preg_replace('/<\s*[0-9A-Fa-f]+\s*>\s*<\s*[0-9A-Fa-f]+\s*>\s*\[[^\]]*\]/', '', $block) ?? $block;
            if (!preg_match_all('/<\s*([0-9A-Fa-f]+)\s*>\s*<\s*([0-9A-Fa-f]+)\s*>\s*<\s*([0-9A-Fa-f\s]+)\s*>/', $plain, $rows, PREG_SET_ORDER)) continue;
            foreach ($rows as $row) $ranges[] = [hexdec($row[1]), hexdec($row[2]), vbd_pdf_hex_to_utf8($row[3])];
        }
    }
    return ['bf' => $bf, 'ranges' => $ranges, 'width' => $width];
}

function vbd_pdf_hex_to_utf8(string $hex): string
{
    $hex = preg_replace('/\s+/', '', $hex) ?? '';
    if ($hex === '') return '';
    if (strlen($hex) % 2) $hex = '0' . $hex;
    $binary = @hex2bin($hex);
    if (!is_string($binary) || $binary === '') return '';
    if (str_starts_with($binary, "\xFE\xFF")) $binary = substr($binary, 2);
    if (strlen($binary) % 2) $binary = substr($binary, 0, -1);
    if ($binary === '') return '';
    if (function_exists('iconv')) {
        $text = @iconv('UTF-16BE', 'UTF-8//IGNORE', $binary);
        if (is_string($text) && $text !== '') return $text;
    }
    $out = '';
    $length = strlen($binary);
    for ($i = 0; $i + 1 < $length; $i += 2) {
        $out .= vbd_pdf_utf8_chr((ord($binary[$i]) << 8) | ord($binary[$i + 1]));
    }
    return $out;
}

function vbd_pdf_utf8_chr(int $code): string
{
    if ($code < 0 || $code > 0x10FFFF || ($code >= 0xD800 && $code <= 0xDFFF)) return '';
    if (function_exists('mb_chr')) {
        $char = mb_chr($code, 'UTF-8');
        return is_string($char) ? $char : '';
    }
    if ($code < 0x80) return chr($code);
    if ($code < 0x800) return chr(0xC0 | ($code >> 6)) . chr(0x80 | ($code & 0x3F));
    if ($code < 0x10000) return chr(0xE0 | ($code >> 12)) . chr(0x80 | (($code >> 6) & 0x3F)) . chr(0x80 | ($code & 0x3F));
    return chr(0xF0 | ($code >> 18)) . chr(0x80 | (($code >> 12) & 0x3F)) . chr(0x80 | (($code >> 6) & 0x3F)) . chr(0x80 | ($code & 0x3F));
}

function vbd_pdf_first_codepoint(string $text): int
{
    if ($text === '') return 0;
    if (function_exists('mb_ord')) return (int)mb_ord($text, 'UTF-8');
    $byte = ord($text[0]);
    if ($byte < 0x80) return $byte;
    if (($byte & 0xE0) === 0xC0 && isset($text[1])) return (($byte & 0x1F) << 6) | (ord($text[1]) & 0x3F);
    if (($byte & 0xF0) === 0xE0 && isset($text[2])) return (($byte & 0x0F) << 12) | ((ord($text[1]) & 0x3F) << 6) | (ord($text[2]) & 0x3F);
    if (($byte & 0xF8) === 0xF0 && isset($text[3])) return (($byte & 0x07) << 18) | ((ord($text[1]) & 0x3F) << 12) | ((ord($text[2]) & 0x3F) << 6) | (ord($text[3]) & 0x3F);
    return $byte;
}

function vbd_pdf_after_first(string $text): string
{
    if ($text === '') return '';
    if (function_exists('mb_substr')) return (string)mb_substr($text, 1, null, 'UTF-8');
    $byte = ord($text[0]);
    $length = 1;
    if ($byte >= 0xF0) $length = 4;
    elseif ($byte >= 0xE0) $length = 3;
    elseif ($byte >= 0xC0) $length = 2;
    return substr($text, $length);
}

function vbd_pdf_map_cid(int $code, array $cmap): string
{
    if (isset($cmap['bf'][$code])) return (string)$cmap['bf'][$code];
    foreach ($cmap['ranges'] as $range) {
        if ($code < $range[0] || $code > $range[1]) continue;
        $dest = $range[2];
        if (is_array($dest)) return (string)($dest[$code - $range[0]] ?? '');
        if (!is_string($dest) || $dest === '') return '';
        return vbd_pdf_utf8_chr(vbd_pdf_first_codepoint($dest) + ($code - $range[0])) . vbd_pdf_after_first($dest);
    }
    return '';
}

function vbd_pdf_winansi(string $bytes): string
{
    if ($bytes === '') return '';
    if (function_exists('iconv')) {
        $text = @iconv('CP1252', 'UTF-8//IGNORE', $bytes);
        if (is_string($text)) return $text;
    }
    return $bytes;
}

function vbd_pdf_decode_text(string $raw, bool $hex, array $font): string
{
    $encoding = (string)($font['enc'] ?? 'utf8');
    $cmap = $font['cmap'] ?? null;
    if ($hex) {
        $clean = preg_replace('/\s+/', '', $raw) ?? '';
        if ($clean === '') return '';
        if (!is_array($cmap)) {
            if ($encoding === 'winansi') {
                $binary = @hex2bin(strlen($clean) % 2 ? '0' . $clean : $clean);
                return is_string($binary) ? vbd_pdf_winansi($binary) : '';
            }
            return vbd_pdf_hex_to_utf8($clean);
        }
        $width = (int)($cmap['width'] ?? 4);
        if ($width < 2) $width = 4;
        if (strlen($clean) % $width !== 0) $width = (strlen($clean) % 4 === 0) ? 4 : 2;
        $text = '';
        $length = strlen($clean);
        for ($i = 0; $i + $width <= $length; $i += $width) {
            $text .= vbd_pdf_map_cid(hexdec(substr($clean, $i, $width)), $cmap);
        }
        return $text;
    }
    if ($encoding === 'winansi') return vbd_pdf_winansi($raw);
    if (is_array($cmap) && $raw !== '') {
        $widthBytes = max(1, intdiv((int)($cmap['width'] ?? 4), 2));
        if (strlen($raw) % $widthBytes === 0 && $widthBytes > 1) {
            $text = '';
            $length = strlen($raw);
            for ($i = 0; $i < $length; $i += $widthBytes) {
                $code = 0;
                for ($j = 0; $j < $widthBytes; $j++) $code = ($code << 8) | ord($raw[$i + $j]);
                $text .= vbd_pdf_map_cid($code, $cmap);
            }
            if ($text !== '') return $text;
        }
    }
    if (preg_match('//u', $raw)) return $raw;
    return vbd_pdf_winansi($raw);
}

function vbd_pdf_content_bytes(array $objects, string $pageDict): string
{
    $ids = [];
    if (preg_match('#/Contents\s*\[(.*?)\]#s', $pageDict, $match)) {
        if (preg_match_all('#(\d+)\s+0\s+R#', $match[1], $refs)) {
            foreach ($refs[1] as $id) $ids[] = (int)$id;
        }
    } elseif (preg_match('#/Contents\s+(\d+)\s+0\s+R#', $pageDict, $match)) {
        $ids[] = (int)$match[1];
    }
    $parts = [];
    foreach ($ids as $id) {
        if (!isset($objects[$id])) continue;
        $body = ltrim($objects[$id]);
        if (str_starts_with($body, '[')) {
            if (preg_match_all('#(\d+)\s+0\s+R#', $body, $refs)) {
                foreach ($refs[1] as $nested) {
                    if (!isset($objects[(int)$nested])) continue;
                    $nestedBody = $objects[(int)$nested];
                    $stream = vbd_pdf_stream($nestedBody);
                    if ($stream !== '') $parts[] = $stream;
                }
            }
            continue;
        }
        $stream = vbd_pdf_stream($body);
        if ($stream !== '') $parts[] = $stream;
    }
    return implode("\n", $parts);
}

function vbd_pdf_xobject_texts(array $objects, int $id, array &$texts, array &$seen, int $depth): void
{
    if ($depth > 6 || $id < 1 || isset($seen[$id]) || !isset($objects[$id])) return;
    $seen[$id] = true;
    $body = $objects[$id];
    $dict = vbd_pdf_dict($body);
    $fonts = vbd_pdf_font_maps($objects, $dict);
    $stream = vbd_pdf_stream($body, $dict);
    if ($stream !== '' && strlen($stream) <= 200000) {
        $text = trim(vbd_pdf_render_content($stream, $fonts));
        if ($text !== '') $texts[] = $text;
    }
    $resourceDict = $dict;
    if (preg_match('#/Resources\s+(\d+)\s+0\s+R#', $dict, $resource) && isset($objects[(int)$resource[1]])) {
        $resourceDict = vbd_pdf_dict($objects[(int)$resource[1]]);
    }
    $xobjects = vbd_pdf_inner_dict($resourceDict, 'XObject');
    if ($xobjects !== '' && preg_match_all('#/[A-Za-z][A-Za-z0-9]*\s+(\d+)\s+0\s+R#', $xobjects, $refs)) {
        foreach ($refs[1] as $ref) vbd_pdf_xobject_texts($objects, (int)$ref, $texts, $seen, $depth + 1);
    }
}

function vbd_pdf_annot_texts(array $objects, string $pageDict, int $pageNumber = 1): array
{
    if ($pageNumber > 2) return [];
    $ids = [];
    if (preg_match('#/Annots\s*\[(.*?)\]#s', $pageDict, $match) && preg_match_all('#(\d+)\s+0\s+R#', $match[1], $refs)) {
        foreach ($refs[1] as $id) $ids[] = (int)$id;
    } elseif (preg_match('#/Annots\s+(\d+)\s+0\s+R#', $pageDict, $match) && isset($objects[(int)$match[1]])) {
        if (preg_match_all('#(\d+)\s+0\s+R#', $objects[(int)$match[1]], $refs)) {
            foreach ($refs[1] as $id) $ids[] = (int)$id;
        }
    }
    $texts = [];
    $seen = [];
    foreach ($ids as $id) {
        if (!isset($objects[$id])) continue;
        $dict = vbd_pdf_dict($objects[$id]);
        if (!preg_match('#/N\s+(\d+)\s+0\s+R#', $dict, $normal)) continue;
        vbd_pdf_xobject_texts($objects, (int)$normal[1], $texts, $seen, 0);
    }
    $clean = [];
    foreach ($texts as $text) {
        $text = trim(preg_replace('/\s+/u', ' ', $text) ?? $text);
        if ($text !== '') $clean[] = $text;
    }
    return $clean;
}

function vbd_pdf_page_text(array $objects, int $pageId, int $pageNumber = 1): string
{
    if (!isset($objects[$pageId])) return '';
    $dict = vbd_pdf_dict($objects[$pageId]);
    $fonts = vbd_pdf_font_maps($objects, $dict);
    $content = vbd_pdf_content_bytes($objects, $dict);
    $rendered = '';
    if ($content !== '') {
        if (strlen($content) > 500000) $content = substr($content, 0, 500000);
        $rendered = vbd_pdf_render_content($content, $fonts);
    }
    $annots = vbd_pdf_annot_texts($objects, $dict, $pageNumber);
    if ($annots) $rendered = 'ANNOT_TEXT: ' . implode(' | ', $annots) . "\n" . $rendered;
    return trim($rendered);
}

function vbd_pdf_read_literal(string $content, int &$index, int $length): string
{
    $buffer = '';
    while ($index < $length) {
        $char = $content[$index];
        if ($char === '\\') {
            $index++;
            if ($index >= $length) break;
            $escaped = $content[$index];
            $map = ['n' => "\n", 'r' => "\r", 't' => "\t", 'b' => "\x08", 'f' => "\f", '(' => '(', ')' => ')', '\\' => '\\'];
            if (isset($map[$escaped])) {
                $buffer .= $map[$escaped];
                $index++;
                continue;
            }
            if ($escaped === "\n") {
                $index++;
                continue;
            }
            if ($escaped === "\r") {
                $index++;
                if ($index < $length && $content[$index] === "\n") $index++;
                continue;
            }
            if ($escaped >= '0' && $escaped <= '7') {
                $octal = $escaped;
                for ($k = 0; $k < 2 && $index + 1 < $length && $content[$index + 1] >= '0' && $content[$index + 1] <= '7'; $k++) {
                    $index++;
                    $octal .= $content[$index];
                }
                $buffer .= chr(octdec($octal) & 255);
                $index++;
                continue;
            }
            $buffer .= $escaped;
            $index++;
            continue;
        }
        if ($char === ')') {
            $index++;
            break;
        }
        $buffer .= $char;
        $index++;
    }
    return $buffer;
}

function vbd_pdf_render_content(string $content, array $fonts): string
{
    $length = strlen($content);
    $index = 0;
    $stack = [];
    $out = [];
    $font = ['enc' => 'utf8', 'cmap' => null];
    $y = null;
    $append = static function (string $text) use (&$out): void {
        if ($text !== '') $out[] = $text;
    };
    $newline = static function () use (&$out): void {
        if (!$out) return;
        $last = $out[count($out) - 1];
        if (!str_ends_with($last, "\n")) $out[] = "\n";
    };
    $noteY = static function (?float $next) use (&$y, $newline): void {
        if ($next === null) return;
        if ($y !== null && abs($next - $y) > 1.8) $newline();
        $y = $next;
    };
    $show = static function (array $token) use (&$font, $append): void {
        $append(vbd_pdf_decode_text($token[1], (bool)$token[2], $font));
    };
    while ($index < $length) {
        $char = $content[$index];
        if ($char === ' ' || $char === "\t" || $char === "\r" || $char === "\n" || $char === "\f") {
            $index++;
            continue;
        }
        if ($char === '%') {
            while ($index < $length && $content[$index] !== "\n" && $content[$index] !== "\r") $index++;
            continue;
        }
        if ($char === '(') {
            $index++;
            $stack[] = ['s', vbd_pdf_read_literal($content, $index, $length), false];
            continue;
        }
        if ($char === '<' && $index + 1 < $length && $content[$index + 1] === '<') {
            $depth = 0;
            while ($index < $length - 1) {
                if ($content[$index] === '<' && $content[$index + 1] === '<') {
                    $depth++;
                    $index += 2;
                    continue;
                }
                if ($content[$index] === '>' && $content[$index + 1] === '>') {
                    $depth--;
                    $index += 2;
                    if ($depth === 0) break;
                    continue;
                }
                $index++;
            }
            continue;
        }
        if ($char === '<') {
            $end = strpos($content, '>', $index + 1);
            if ($end === false) break;
            $stack[] = ['s', substr($content, $index + 1, $end - $index - 1), true];
            $index = $end + 1;
            continue;
        }
        if ($char === '[') {
            $index++;
            $items = [];
            while ($index < $length && $content[$index] !== ']') {
                $item = $content[$index];
                if ($item === ' ' || $item === "\t" || $item === "\r" || $item === "\n") {
                    $index++;
                    continue;
                }
                if ($item === '(') {
                    $index++;
                    $items[] = ['s', vbd_pdf_read_literal($content, $index, $length), false];
                    continue;
                }
                if ($item === '<') {
                    $end = strpos($content, '>', $index + 1);
                    if ($end === false) break 2;
                    $items[] = ['s', substr($content, $index + 1, $end - $index - 1), true];
                    $index = $end + 1;
                    continue;
                }
                if (preg_match('/[+-]?(?:\d+\.\d*|\.\d+|\d+)/A', $content, $number, 0, $index)) {
                    $items[] = ['n', (float)$number[0]];
                    $index += strlen($number[0]);
                    continue;
                }
                $index++;
            }
            if ($index < $length && $content[$index] === ']') $index++;
            $stack[] = ['r', $items, false];
            continue;
        }
        if ($char === '/') {
            if (!preg_match('#/[^\s/\[\]()<>{}%]+#A', $content, $name, 0, $index)) {
                $index++;
                continue;
            }
            $stack[] = ['a', substr($name[0], 1), false];
            $index += strlen($name[0]);
            continue;
        }
        if (preg_match('/[+-]?(?:\d+\.\d*|\.\d+|\d+)/A', $content, $number, 0, $index)) {
            $stack[] = ['n', (float)$number[0], false];
            $index += strlen($number[0]);
            continue;
        }
        if (!preg_match('/[A-Za-z*\'"]+/A', $content, $operator, 0, $index)) {
            $index++;
            continue;
        }
        $op = $operator[0];
        $index += strlen($op);
        if ($op === 'Tf') {
            for ($k = count($stack) - 1; $k >= 0; $k--) {
                if ($stack[$k][0] === 'a') {
                    $font = $fonts[$stack[$k][1]] ?? $font;
                    break;
                }
            }
            $stack = [];
            continue;
        }
        if ($op === 'Tm') {
            $numbers = array_values(array_filter($stack, static fn(array $item): bool => $item[0] === 'n'));
            if (count($numbers) >= 6) $noteY((float)$numbers[count($numbers) - 1][1]);
            $stack = [];
            continue;
        }
        if ($op === 'Td' || $op === 'TD') {
            $numbers = array_values(array_filter($stack, static fn(array $item): bool => $item[0] === 'n'));
            if (count($numbers) >= 2) {
                $dy = (float)$numbers[count($numbers) - 1][1];
                if (abs($dy) > 1.8) {
                    $newline();
                    $y = $y === null ? $dy : $y + $dy;
                }
            }
            $stack = [];
            continue;
        }
        if ($op === 'T*') {
            $newline();
            $stack = [];
            continue;
        }
        if ($op === 'BT' || $op === 'ET') {
            $newline();
            $stack = [];
            continue;
        }
        if ($op === "'" || $op === '"') {
            $newline();
            for ($k = count($stack) - 1; $k >= 0; $k--) {
                if ($stack[$k][0] === 's') {
                    $show($stack[$k]);
                    break;
                }
            }
            $stack = [];
            continue;
        }
        if ($op === 'Tj') {
            for ($k = count($stack) - 1; $k >= 0; $k--) {
                if ($stack[$k][0] === 's') {
                    $show($stack[$k]);
                    break;
                }
            }
            $stack = [];
            continue;
        }
        if ($op === 'TJ' && $stack && $stack[count($stack) - 1][0] === 'r') {
            foreach ($stack[count($stack) - 1][1] as $item) {
                if ($item[0] === 's') $show($item);
                elseif ($item[0] === 'n' && (float)$item[1] < -120) {
                    $last = $out ? $out[count($out) - 1] : '';
                    if ($last !== '' && !str_ends_with($last, ' ') && !str_ends_with($last, "\n")) $out[] = ' ';
                }
            }
            $stack = [];
            continue;
        }
        $stack = [];
    }
    return implode('', $out);
}

function vbd_pdf_clean_text(string $text): string
{
    $text = str_replace(["\r\n", "\r"], "\n", $text);
    $text = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F]/', '', $text) ?? $text;
    $text = preg_replace('/[ \t]{2,}/u', ' ', $text) ?? $text;
    $text = preg_replace('/[ \t]+\n/u', "\n", $text) ?? $text;
    $text = preg_replace("/\n{3,}/", "\n\n", $text) ?? $text;
    return trim($text);
}
