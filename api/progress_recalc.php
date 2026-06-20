<?php

function pr_decode_json_array($value): array
{
    if ($value === null || $value === '') return [];
    $decoded = json_decode($value, true);
    return is_array($decoded) ? $decoded : [];
}

function pr_split_pool_text_by_gt(string $source): array
{
    if ($source === '') return [];

    $parts = [];
    $current = '';
    $length = strlen($source);
    $inInlineMath = false;
    $inDisplayMath = false;

    for ($i = 0; $i < $length; $i += 1) {
        if (!$inInlineMath && $i + 1 < $length && substr($source, $i, 2) === '$$') {
            $inDisplayMath = !$inDisplayMath;
            $current .= '$$';
            $i += 1;
            continue;
        }
        if (!$inDisplayMath && $source[$i] === '$') {
            $inInlineMath = !$inInlineMath;
            $current .= '$';
            continue;
        }
        if ($source[$i] === '>' && !$inInlineMath && !$inDisplayMath) {
            $trimmed = trim($current);
            if ($trimmed !== '') $parts[] = $trimmed;
            $current = '';
            continue;
        }
        $current .= $source[$i];
    }

    $trimmed = trim($current);
    if ($trimmed !== '') $parts[] = $trimmed;
    return $parts;
}

function pr_split_pool_text($value): array
{
    $source = (string)$value;
    if ($source === '') return [];
    if (preg_match('/\s*»\s*/u', $source)) {
        $parts = preg_split('/\s*»\s*/u', $source) ?: [];
        $items = [];
        foreach ($parts as $part) {
            $part = trim((string)$part);
            if ($part !== '') $items[] = $part;
        }
        return $items;
    }
    return pr_split_pool_text_by_gt($source);
}

function pr_repair_pool_pieces(array $pieces, int $expectedCount = 0): array
{
    if (count($pieces) <= 1) return $pieces;
    $repaired = pr_split_pool_text(implode(' > ', $pieces));
    if (count($repaired) >= count($pieces)) return $pieces;
    if ($expectedCount > 0 && count($repaired) === $expectedCount) return $repaired;
    if ($expectedCount === 0 && count($repaired) < count($pieces)) return $repaired;
    return $pieces;
}

function pr_normalize_answer_text($value): string
{
    $text = trim((string)$value);
    $map = [
        '∈' => '\\in', '∉' => '\\notin', '⊂' => '\\subset', '⊆' => '\\subseteq',
        '∪' => '\\cup', '∩' => '\\cap', '∅' => '\\emptyset', '×' => '\\times',
        '÷' => '\\div', '≤' => '\\leq', '≥' => '\\geq', '≠' => '\\neq',
        'π' => '\\pi', '∞' => '\\infty', '√' => '\\sqrt',
    ];
    $text = strtr($text, $map);
    $text = mb_strtolower($text, 'UTF-8');
    $text = preg_replace('/\s+/u', '', $text) ?? '';
    return $text;
}

function pr_count_blank_tokens(string $prompt): int
{
    $count = preg_match_all('/_{3,}|\[\.\.\.\]|\[\s*\]/u', $prompt, $matches);
    return max(1, (int)$count);
}

function pr_normalize_fill_exercise(array $item): array
{
    $prompt = (string)($item['prompt'] ?? '');
    $blankCount = pr_count_blank_tokens($prompt);
    $pool = is_array($item['items'] ?? null) ? $item['items'] : pr_split_pool_text($item['pool'] ?? '');
    $answers = [];
    if (is_array($item['answer'] ?? null)) {
        $answers = array_values(array_filter(array_map('trim', $item['answer']), fn($v) => $v !== ''));
    } elseif (str_contains((string)($item['answer'] ?? ''), '>')) {
        $answers = pr_split_pool_text($item['answer']);
    } elseif (!empty($item['answer'])) {
        $answers = [trim((string)$item['answer'])];
    }
    if (!$pool && $answers) $pool = $answers;
    while (count($answers) < $blankCount && $answers) {
        $answers[] = $answers[count($answers) - 1];
    }
    if (!$answers && $pool) $answers = [$pool[0]];
    return [
        'id' => $item['id'] ?? '',
        'blankCount' => $blankCount,
        'answers' => array_slice($answers, 0, $blankCount),
    ];
}

function pr_parse_match_pairs($spec): array
{
    $pairs = [];
    foreach (preg_split('/\s*,\s*/', (string)$spec) ?: [] as $part) {
        $part = trim($part);
        if ($part === '') continue;
        $bits = preg_split('/\s*-\s*/', $part);
        if (count($bits) < 2) continue;
        $left = (int)$bits[0];
        $right = (int)$bits[1];
        $pairs[] = ['left' => $left, 'right' => $right];
    }
    return $pairs;
}

function pr_normalize_drag_exercise(array $item): array
{
    if (($item['mode'] ?? '') === 'match' || (is_array($item['left'] ?? null) && is_array($item['right'] ?? null))) {
        $pairs = is_array($item['pairs'] ?? null) && $item['pairs']
            ? $item['pairs']
            : pr_parse_match_pairs($item['pair_spec'] ?? $item['pairs_text'] ?? '');
        $pairCount = count($pairs);
        $left = pr_repair_pool_pieces(is_array($item['left'] ?? null) ? $item['left'] : [], $pairCount);
        $right = pr_repair_pool_pieces(is_array($item['right'] ?? null) ? $item['right'] : [], $pairCount);
        return [
            'id' => $item['id'] ?? '',
            'mode' => 'match',
            'left' => $left,
            'right' => $right,
            'pairs' => $pairs,
        ];
    }
    $items = is_array($item['items'] ?? null) ? $item['items'] : pr_split_pool_text($item['items_text'] ?? '');
    $answer = is_array($item['answer'] ?? null) ? $item['answer'] : pr_split_pool_text($item['answer_text'] ?? $item['answer'] ?? '');
    $cleanItems = [];
    foreach ($items as $piece) {
        $piece = trim((string)$piece);
        if ($piece !== '') $cleanItems[] = $piece;
    }
    return [
        'id' => $item['id'] ?? '',
        'mode' => 'sort',
        'items' => $cleanItems,
        'answer' => $answer,
    ];
}

function pr_sort_piece_index($piece, array $items): int
{
    $key = pr_normalize_answer_text($piece);
    foreach ($items as $index => $item) {
        if (pr_normalize_answer_text($item) === $key) return (int)$index;
    }
    return -1;
}

function pr_is_sort_answer_correct(array $normalized, array $savedOrder): bool
{
    if (!$savedOrder || count($savedOrder) < count($normalized['items'])) return false;
    $expected = [];
    foreach ($normalized['answer'] as $answer) {
        $expected[] = pr_sort_piece_index($answer, $normalized['items']);
    }
    $given = [];
    foreach ($savedOrder as $piece) {
        $given[] = pr_sort_piece_index($piece, $normalized['items']);
    }
    if ($expected && $given && !in_array(-1, $expected, true) && !in_array(-1, $given, true)) {
        return implode('|', $expected) === implode('|', $given);
    }
    $expectedText = array_map('pr_normalize_answer_text', $normalized['answer']);
    $givenText = array_map('pr_normalize_answer_text', $savedOrder);
    return implode('|', $expectedText) === implode('|', $givenText);
}

function pr_evaluate_mcq(array $lesson, array $state): ?int
{
    $questions = pr_decode_json_array($lesson['questions_json'] ?? null);
    if (!$questions) return null;
    $answers = is_array($state['answers'] ?? null) ? $state['answers'] : [];
    $correct = 0;
    foreach ($questions as $question) {
        $qid = $question['id'] ?? '';
        $selected = isset($answers[$qid]) ? (int)$answers[$qid] : -1;
        $expected = isset($question['answer']) ? (int)$question['answer'] : -1;
        if ($selected === $expected) $correct += 1;
    }
    return (int)round(($correct / count($questions)) * 100);
}

function pr_evaluate_essay(array $lesson, array $state): ?int
{
    $items = pr_decode_json_array($lesson['essay_json'] ?? null);
    if (!$items) return null;
    $answers = is_array($state['essayAnswers'] ?? null) ? $state['essayAnswers'] : [];
    $correct = 0;
    foreach ($items as $index => $item) {
        $key = $item['id'] ?? ('essay_' . ($index + 1));
        $value = pr_normalize_answer_text($answers[$key] ?? '');
        $expected = pr_normalize_answer_text($item['answer'] ?? '');
        if ($expected !== '' && $value === $expected) $correct += 1;
    }
    return (int)round(($correct / count($items)) * 100);
}

function pr_evaluate_fill(array $lesson, array $state): ?int
{
    $items = pr_decode_json_array($lesson['fill_json'] ?? null);
    if (!$items) return null;
    $answers = is_array($state['fillAnswers'] ?? null) ? $state['fillAnswers'] : [];
    $correct = 0;
    foreach ($items as $index => $item) {
        $normalized = pr_normalize_fill_exercise($item);
        $key = $normalized['id'] ?: ($item['id'] ?? ('fill_' . ($index + 1)));
        $slots = $answers[$key] ?? [];
        if (!is_array($slots)) $slots = [trim((string)$slots)];
        $given = array_map('pr_normalize_answer_text', $slots);
        $expected = array_map('pr_normalize_answer_text', $normalized['answers']);
        if ($expected && count($given) >= count($expected)) {
            $ok = true;
            foreach ($expected as $slotIndex => $answer) {
                if (($given[$slotIndex] ?? '') !== $answer) {
                    $ok = false;
                    break;
                }
            }
            if ($ok) $correct += 1;
        }
    }
    return (int)round(($correct / count($items)) * 100);
}

function pr_evaluate_drag(array $lesson, array $state): ?int
{
    $items = pr_decode_json_array($lesson['drag_json'] ?? null);
    if (!$items) return null;
    $answers = is_array($state['dragAnswers'] ?? null) ? $state['dragAnswers'] : [];
    $correct = 0;
    foreach ($items as $index => $item) {
        $normalized = pr_normalize_drag_exercise($item);
        $key = $normalized['id'] ?: ($item['id'] ?? ('drag_' . ($index + 1)));
        $saved = $answers[$key] ?? null;
        if (is_object($saved)) $saved = (array)$saved;
        if ($normalized['mode'] === 'match') {
            $matches = is_array($saved) && !array_is_list($saved) ? $saved : [];
            $ok = true;
            foreach ($normalized['pairs'] as $pair) {
                $left = (int)($pair['left'] ?? -1);
                $right = (int)($pair['right'] ?? -1);
                if ((int)($matches[$left] ?? $matches[(string)$left] ?? -1) !== $right) {
                    $ok = false;
                    break;
                }
            }
            if ($ok && $normalized['pairs']) $correct += 1;
            continue;
        }
        $savedOrder = is_array($saved) ? $saved : [];
        if (pr_is_sort_answer_correct($normalized, $savedOrder)) $correct += 1;
    }
    return (int)round(($correct / count($items)) * 100);
}

function pr_merged_practice_score(array $lesson, array $state): ?int
{
    $parts = array_values(array_filter([
        pr_evaluate_mcq($lesson, $state),
        pr_evaluate_essay($lesson, $state),
        pr_evaluate_fill($lesson, $state),
        pr_evaluate_drag($lesson, $state),
    ], fn($score) => $score !== null));
    if (!$parts) return null;
    return (int)round(array_sum($parts) / count($parts));
}

function pr_lesson_skill_scores(array $lesson, int $percent): array
{
    $skills = pr_decode_json_array($lesson['skills_json'] ?? null);
    $scores = [];
    foreach ($skills as $skill) {
        $id = $skill['id'] ?? '';
        if ($id !== '') $scores[$id] = $percent;
    }
    return $scores;
}

function pr_derive_status(array $state, int $score): string
{
    if (!empty($state['practiceDone'])) {
        if ($score >= 80) return 'mastered';
        if ($score >= 50) return 'needs_practice';
        return 'in_progress';
    }
    if (!empty($state['theoryDone']) || !empty($state['examplesDone']) || !empty($state['startedAt'])) {
        return 'in_progress';
    }
    return 'not_started';
}

function pr_recalc_progress_row(array $lesson, array $progressRow): array
{
    $state = pr_decode_json_array($progressRow['state_json'] ?? null);
    $oldScore = (int)($progressRow['score'] ?? 0);
    $oldStatus = (string)($progressRow['status'] ?? 'not_started');

    if (!empty($state['practiceDone'])) {
        $merged = pr_merged_practice_score($lesson, $state);
        $declared = isset($state['practiceScore']) ? (int)$state['practiceScore'] : null;
        if ($declared !== null && $declared >= 0 && $declared <= 100) {
            $score = $declared;
        } else {
            $score = $merged !== null ? $merged : $oldScore;
        }
        $status = pr_derive_status($state, $score);
        $skillScores = pr_lesson_skill_scores($lesson, $score);
        $completedAt = $progressRow['completed_at'] ?? ($state['completedAt'] ?? null);
    } else {
        $score = $oldScore;
        $status = pr_derive_status($state, $score);
        $skillScores = pr_decode_json_array($progressRow['skill_scores_json'] ?? null);
        $completedAt = null;
    }

    return [
        'score' => max(0, min(100, $score)),
        'status' => $status,
        'skill_scores' => $skillScores,
        'completed_at' => $completedAt,
        'changed' => $score !== $oldScore || $status !== $oldStatus,
    ];
}

function pr_recalc_lesson_progress(PDO $pdo, array $lesson, ?array $teacherUser = null): array
{
    $lessonId = (int)$lesson['id'];
    $stmt = $pdo->prepare('SELECT * FROM student_lesson_progress WHERE lesson_id = ?');
    $stmt->execute([$lessonId]);
    $rows = $stmt->fetchAll();

    $updated = 0;
    $checked = 0;
    foreach ($rows as $row) {
        if ($teacherUser) {
            $studentStmt = $pdo->prepare('SELECT class_name FROM users WHERE id = ? AND role = ? LIMIT 1');
            $studentStmt->execute([(int)$row['student_id'], 'student']);
            $student = $studentStmt->fetch();
            if (!$student || !teacher_can_view_student_class($teacherUser, (string)($student['class_name'] ?? ''))) {
                continue;
            }
        }

        $checked += 1;
        $next = pr_recalc_progress_row($lesson, $row);
        $update = $pdo->prepare('
            UPDATE student_lesson_progress
            SET status = ?, score = ?, skill_scores_json = ?, completed_at = ?
            WHERE id = ?
        ');
        $update->execute([
            $next['status'],
            $next['score'],
            json_encode($next['skill_scores'], JSON_UNESCAPED_UNICODE),
            $next['completed_at'],
            (int)$row['id'],
        ]);
        if ($next['changed']) $updated += 1;
    }

    return [
        'lesson_id' => $lessonId,
        'checked' => $checked,
        'updated' => $updated,
    ];
}