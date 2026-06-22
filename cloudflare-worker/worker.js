const DEFAULT_MODEL = '@cf/qwen/qwen3-30b-a3b-fp8';
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
  const mode = body.mode === 'chat' ? 'chat' : (body.mode === 'document' ? 'document' : 'explain');
  const subject = text(body.subject || 'Toán', 80);
  const lessonTitle = text(body.lesson_title || 'Bài học', 180);
  const selectedText = text(body.text);
  const question = text(body.question);
  const lessonContext = text(body.lesson_context, MAX_CONTEXT_CHARS);

  if (mode === 'document') {
    return [
      {
        role: 'system',
        content: [
          'Bạn là trợ lý trích xuất văn bản hành chính Việt Nam. Nhiệm vụ: CHỈ trích xuất của VĂN BẢN CHÍNH ở phần ĐẦU. Bỏ qua mọi số/ngày của văn bản được trích dẫn bên trong.',
          'QUY TẮC BẮT BUỘC:',
          '- document_number: Tìm số sau "Số:" (ví dụ 1176/UBND-VHXH). Nếu "Số:" và số bị tách (do text layer/OCR/ký số), vẫn lấy số dạng NNNN/XXXX gần "Số" hoặc tên cơ quan ở trên cùng. KHÔNG lấy số sau "Căn cứ", "Trên cơ sở", "Công văn số", "theo".',
          '- BỎ QUA hoàn toàn chữ ký số, ngày ký, "Ký bởi".',
          '- document_date: NGÀY BAN HÀNH ở góc phải trên cùng ("Hồ Nai, ngày 22 tháng 6 năm 2026").',
          '- organization: Tên cơ quan ban hành (ỦY BAN NHÂN DÂN PHƯỜNG HỐ NAI...).',
          '- title: Sau "V/v" hoặc "Về việc".',
          'Trả về DUY NHẤT JSON hợp lệ.',
          'Fields: document_number, title, organization, document_type, summary_text, document_date (YYYY-MM-DD hoặc null), report_required, report_due_at, confidence, note.',
        ].join(' '),
      },
      {
        role: 'user',
        content: `Văn bản (chỉ lấy số chính sau Số:, ngày ban hành, cơ quan, trích yếu. Bỏ tham chiếu và chữ ký số):\n${selectedText}`,
      },
    ];
  }

  const system = [
    'Bạn là giáo viên Toán THCS giải thích cho học sinh lớp 6-9.',
    'Mục tiêu chính: giúp học sinh HIỂU RÕ chính xác đoạn nội dung họ vừa chọn, không làm rối thêm.',
    'Quy tắc BẮT BUỘC:',
    '- Luôn bám sát 100% đoạn văn bản học sinh cung cấp. Không lan man, không thêm kiến thức ngoài bài.',
    '- Giải thích bằng tiếng Việt đơn giản, câu ngắn, từ dễ hiểu với học sinh THCS.',
    '- Cấu trúc giải thích rõ ràng: 1) Đoạn này nói gì (nghĩa trực tiếp)? 2) Ý quan trọng nhất là gì? 3) Liên hệ nhanh với bài học.',
    '- Tránh hoàn toàn các từ mơ hồ: có thể, thường thì, nói chung, hầu như, về cơ bản, đôi khi.',
    '- Nếu là khái niệm: dùng "nghĩa là...", "được hiểu là...".',
    '- Nếu là công thức: giải thích từng ký hiệu và cách dùng.',
    '- Không dùng Markdown, không tiêu đề, không **, không chào hỏi dài.',
    '- Giữ nguyên ký hiệu Toán và LaTeX. Trả lời tối đa 5-7 câu ngắn, kết thúc rõ ràng bằng dấu chấm.',
  ].join(' ');

  const messages = [{ role: 'system', content: system }];
  if (lessonContext) {
    messages.push({
      role: 'system',
      content: `Ngữ cảnh bài đang học (${subject} — ${lessonTitle}):\n${lessonContext}\n\nKhi giải thích, ưu tiên dùng các ý, định nghĩa có trong ngữ cảnh này nếu phù hợp với đoạn được hỏi.`,
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
    ? `Câu hỏi của học sinh: ${question}\n\nChỉ trả lời đúng câu hỏi này, bám sát bài đang học.`
    : `Học sinh đang học bài "${lessonTitle}" và cần giải thích RÕ RÀNG, CỤ THỂ đoạn sau (không lan man, không thêm ý ngoài):\n\n${selectedText}`;
  messages.push({ role: 'user', content: userPrompt });
  return messages;
}

function extractAnswer(result) {
  if (typeof result?.response === 'string') return result.response.trim();
  if (typeof result?.result?.response === 'string') return result.result.response.trim();
  if (typeof result?.choices?.[0]?.message?.content === 'string') return result.choices[0].message.content.trim();
  return '';
}

function selectedModel(body, env) {
  const requested = String(body?.model || '');
  if (/^@cf\/[a-z0-9._-]+\/[a-z0-9._-]+$/i.test(requested)) return requested;
  const configured = String(env.AI_MODEL || DEFAULT_MODEL);
  return /^@cf\/[a-z0-9._-]+\/[a-z0-9._-]+$/i.test(configured) ? configured : DEFAULT_MODEL;
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

    const mode = body?.mode === 'chat' ? 'chat' : (body?.mode === 'document' ? 'document' : 'explain');
    if ((mode === 'chat' && !text(body?.question)) || (mode !== 'chat' && !text(body?.text))) {
      return json({ error: 'Thiếu nội dung cần AI trả lời.' }, 422);
    }

    try {
      const model = selectedModel(body, env);
      const result = await env.AI.run(model, {
        messages: buildMessages(body),
        temperature: 0.25,
        max_tokens: mode === 'document' ? 680 : 420,
      });
      const answer = extractAnswer(result);
      if (!answer) {
        return json({ error: 'Workers AI trả về nội dung rỗng.', code: 'empty_response' }, 502);
      }
      const usage = result?.usage && typeof result.usage === 'object'
        ? {
            prompt_tokens: Number(result.usage.prompt_tokens || result.usage.input_tokens || 0),
            completion_tokens: Number(result.usage.completion_tokens || result.usage.output_tokens || 0),
            total_tokens: Number(result.usage.total_tokens || 0),
          }
        : null;
      return json({
        ok: true,
        answer,
        provider: 'cloudflare_workers_ai',
        model,
        ...(usage ? { usage } : {}),
      });
    } catch (error) {
      const detail = text(error?.message || error, 300) || 'Lỗi không xác định.';
      console.error('Workers AI failed', detail);
      return json({
        error: `Workers AI lỗi: ${detail}`,
        code: 'workers_ai_unavailable',
      }, 502);
    }
  },
};
