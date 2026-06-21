const DEFAULT_MODEL = '@cf/meta/llama-3.1-8b-instruct';
const MAX_CONTEXT_CHARS = 2600;
const MAX_MESSAGE_CHARS = 1200;
const MAX_HISTORY_TURNS = 6;

function json(payload, status = 200) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: {
      'content-type': 'application/json; charset=UTF-8',
      'cache-control': 'no-store',
    },
  });
}

function text(value, maxLength = MAX_MESSAGE_CHARS) {
  return String(value || '').replace(/\s+/g, ' ').trim().slice(0, maxLength);
}

function authorized(request, env) {
  const expected = String(env.APP_SHARED_SECRET || '');
  const supplied = String(request.headers.get('X-Giangbai-Worker-Secret') || '');
  return expected !== '' && supplied !== '' && supplied === expected;
}

function buildMessages(body) {
  const mode = body.mode === 'chat' ? 'chat' : 'explain';
  const subject = text(body.subject || 'Toán', 80);
  const lessonTitle = text(body.lesson_title || 'Bài học', 180);
  const selectedText = text(body.text);
  const question = text(body.question);
  const lessonContext = text(body.lesson_context, MAX_CONTEXT_CHARS);

  const system = [
    'Bạn là trợ lý học Toán THCS bằng tiếng Việt.',
    'Giải thích rõ, chính xác và thân thiện; ưu tiên kiến thức Toán.',
    'Với bài tập, hướng dẫn từng bước ngắn gọn và nêu kết quả khi học sinh yêu cầu giải.',
    'Không bịa nội dung bài học. Nếu thiếu dữ kiện, hãy nói rõ phần còn thiếu.',
    'Không chào dài, không dùng Markdown thô, không dùng tiêu đề, không dùng ký tự **.',
    'Giữ ký hiệu Toán và LaTeX nếu có. Trả lời tối đa 6 câu ngắn.',
  ].join(' ');

  const messages = [{ role: 'system', content: system }];
  if (lessonContext) {
    messages.push({
      role: 'system',
      content: `Ngữ cảnh bài đang học (${subject} — ${lessonTitle}):\n${lessonContext}`,
    });
  }

  if (mode === 'chat' && Array.isArray(body.history)) {
    body.history.slice(-MAX_HISTORY_TURNS).forEach((turn) => {
      const role = turn?.role === 'assistant' ? 'assistant' : 'user';
      const content = text(turn?.content, 700);
      if (content) messages.push({ role, content });
    });
  }

  const userPrompt = mode === 'chat'
    ? `Câu hỏi mới của học sinh: ${question}`
    : `Hãy giải thích phần sau trong bài ${lessonTitle}: ${selectedText}`;
  messages.push({ role: 'user', content: userPrompt });
  return messages;
}

function extractAnswer(result) {
  if (typeof result?.response === 'string') return result.response.trim();
  if (typeof result?.result?.response === 'string') return result.result.response.trim();
  if (typeof result?.choices?.[0]?.message?.content === 'string') return result.choices[0].message.content.trim();
  return '';
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'GET' && url.pathname === '/') {
      return json({
        ok: true,
        service: 'GiangBai Workers AI',
        configured: Boolean(env.AI && env.APP_SHARED_SECRET),
      });
    }

    if (request.method !== 'POST' || url.pathname !== '/chat') {
      return json({ error: 'Not found.' }, 404);
    }
    if (!authorized(request, env)) {
      return json({ error: 'Unauthorized.' }, 401);
    }
    if (!env.AI) {
      return json({ error: 'Workers AI binding AI chưa được cấu hình.' }, 503);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: 'Dữ liệu JSON không hợp lệ.' }, 400);
    }

    const mode = body?.mode === 'chat' ? 'chat' : 'explain';
    if ((mode === 'chat' && !text(body?.question)) || (mode !== 'chat' && !text(body?.text))) {
      return json({ error: 'Thiếu nội dung cần AI trả lời.' }, 422);
    }

    try {
      const model = String(env.AI_MODEL || DEFAULT_MODEL);
      const result = await env.AI.run(model, {
        messages: buildMessages(body),
        temperature: 0.25,
        max_tokens: 360,
      });
      const answer = extractAnswer(result);
      if (!answer) {
        return json({ error: 'Workers AI trả về nội dung rỗng.', code: 'empty_response' }, 502);
      }
      return json({
        ok: true,
        answer,
        provider: 'cloudflare_workers_ai',
        model,
      });
    } catch (error) {
      console.error('Workers AI failed', error?.message || error);
      return json({ error: 'Workers AI hiện không phản hồi.', code: 'workers_ai_unavailable' }, 502);
    }
  },
};
