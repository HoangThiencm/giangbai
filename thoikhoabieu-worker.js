/** Web Worker — xếp TKB ngoài main thread */
importScripts('./thoikhoabieu-engine.js');
self.onmessage = function (ev) {
  var msg = ev.data || {};
  if (msg.type !== 'solve') return;
  try {
    var t0 = Date.now();
    var result = self.TkbEngine.solveSnapshot(msg.payload || {});
    self.postMessage({
      type: 'solve-done',
      requestId: msg.requestId,
      ok: true,
      result: {
        ok: result.ok,
        status: result.status,
        precheckIssues: result.precheckIssues,
        assignments: result.assignments,
        nodes: result.nodes,
        deepest: result.deepest,
        blockedLesson: result.blockedLesson,
        beauty: result.beauty,
        audit: result.audit,
        total: result.total,
        placed: result.placed,
        ms: Date.now() - t0
      },
      lessons: (result.lessons || []).map(function (L) {
        return {
          id: L.id, classId: L.classId, teacherId: L.teacherId,
          subject: L.subject, className: L.className, teacherName: L.teacherName,
          roomNeed: L.roomNeed || '', unit: L.unit
        };
      })
    });
  } catch (err) {
    self.postMessage({
      type: 'solve-done', requestId: msg.requestId, ok: false,
      error: String(err && err.message ? err.message : err)
    });
  }
};
