"""Cầu nối chạy ngầm agy.exe trong QThread, không khóa giao diện."""

from __future__ import annotations

import json
import queue
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from core.preflight import find_agy, writable_dir

CREATE_NO_WINDOW = 0x08000000
PERCENT = re.compile(r"(?<!\d)(100|[1-9]?\d)\s*%")
RESULT_LINE = re.compile(r"KET_QUA:\s*(.+)", re.IGNORECASE)
HEARTBEAT_SECONDS = 3.0


def build_agy_command(agy: str, prompt_path: Path, model: str = "") -> list[str]:
    """Lệnh agy -p tiếng Anh, stream-json, kèm --model khi người dùng đã chọn."""
    instruction = (
        "Read the following UTF-8 file and follow all instructions strictly without asking. "
        "Do not open browser. File: "
        f"{prompt_path}"
    )
    command = [
        agy,
        "-p",
        instruction,
        "--disable-slash-commands",
        "--dangerously-skip-permissions",
        "--output-format",
        "stream-json",
    ]
    chosen = (model or "").strip()
    if chosen:
        command.extend(["--model", chosen])
    return command


class StreamWatch:
    """Trạng thái đọc NDJSON: bước, phần trăm, log và đường dẫn KET_QUA."""

    def __init__(self) -> None:
        self.step_counter = 0
        self.last_index = None
        self.captured = ""
        self.progress = 3
        self.logs: list[str] = []
        self.raw_lines = 0
        self.saw_result = False


def _event_name(data: dict) -> str:
    event = data.get("event")
    if isinstance(event, str) and event.strip():
        return event.strip()
    if isinstance(event, dict):
        for key in ("step_update", "text_delta", "thinking_delta", "result", "init"):
            if key in event:
                return key
    for key in ("type", "kind"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    for key in ("step_update", "text_delta", "thinking_delta", "result", "init"):
        if key in data:
            return key
    return ""


def _payload(data: dict, event: str) -> dict:
    wrapped = data.get("event")
    if isinstance(wrapped, dict):
        nested = wrapped.get(event)
        if isinstance(nested, dict):
            return nested
    nested = data.get(event)
    if isinstance(nested, dict):
        return nested
    return data


def _capture_result(text: str, watch: StreamWatch) -> None:
    match = RESULT_LINE.search(text or "")
    if match:
        watch.captured = match.group(1).strip().strip('"')


def _raise_progress(watch: StreamWatch, percent: int) -> None:
    percent = max(0, min(100, int(percent)))
    if percent > watch.progress:
        watch.progress = percent


def _delta_text(update: dict, data: dict, event: str) -> str:
    for source in (update, data):
        for key in ("text_delta", "textDelta", "thinking_delta", "thinkingDelta", "text", "delta"):
            value = source.get(key)
            if isinstance(value, str) and value:
                return value
    direct = data.get(event)
    if isinstance(direct, str):
        return direct
    return ""


def interpret_stream_line(line: str, watch: StreamWatch) -> None:
    """Một dòng stdout: NDJSON thì tăng bước, không thì vẫn đẩy log và phần trăm."""
    line = (line or "").strip()
    if not line:
        return
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        watch.raw_lines += 1
        watch.logs.append(line)
        _capture_result(line, watch)
        found = PERCENT.findall(line)
        percent = int(found[-1]) if found else min(92, 8 + watch.raw_lines)
        _raise_progress(watch, percent)
        return
    if not isinstance(data, dict):
        watch.logs.append(line)
        return

    event = _event_name(data)
    if event == "init":
        watch.logs.append("Đã bắt đầu phiên AI.")
        _raise_progress(watch, 8)
        return
    if event == "step_update":
        update = _payload(data, "step_update")
        raw_index = update.get("step_index", update.get("stepIndex", None))
        if raw_index is None:
            watch.step_counter += 1
            step_idx = watch.step_counter
        else:
            step_idx = raw_index
            if step_idx != watch.last_index:
                watch.step_counter += 1
                watch.last_index = step_idx
        step_type = str(update.get("step_type", update.get("stepType", "")) or "")
        delta = _delta_text(update, data, event)
        _raise_progress(watch, min(92, 5 + int(watch.step_counter * 3)))
        if delta.strip():
            watch.logs.append(delta.strip())
            _capture_result(delta, watch)
        else:
            label = f"Đang thực hiện bước {step_idx}"
            if step_type:
                label += f" ({step_type})"
            watch.logs.append(label + "…")
        return
    if event in {"text_delta", "thinking_delta"}:
        update = _payload(data, event)
        delta = _delta_text(update, data, event)
        if delta.strip():
            watch.logs.append(delta.strip())
            _capture_result(delta, watch)
        return
    if event == "result":
        result_data = _payload(data, "result")
        resp = result_data.get("response", result_data.get("text", ""))
        if not isinstance(resp, str):
            resp = json.dumps(resp, ensure_ascii=False) if resp else ""
        watch.saw_result = True
        _capture_result(resp, watch)
        if resp.strip() and len(resp.strip()) <= 500:
            watch.logs.append(resp.strip())
        elif resp.strip():
            watch.logs.append("Đã nhận kết quả từ AI.")
        _raise_progress(watch, 100)
        return

    text = data.get("text") or data.get("message") or ""
    if isinstance(text, str) and text.strip():
        watch.logs.append(text.strip())
        _capture_result(text, watch)


def _newest_file(directory: Path, since: float) -> Path | None:
    if not directory.is_dir():
        return None
    found: list[Path] = []
    for path in directory.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in {".tmp", ".partial"}:
            continue
        try:
            if path.stat().st_mtime >= since - 1:
                found.append(path)
        except OSError:
            continue
    if not found:
        return None
    return max(found, key=lambda item: item.stat().st_mtime)


class AntigravityWorker(QThread):
    """Chạy một lượt agy -p và phát log, tiến độ, đường dẫn kết quả."""

    signal_log = Signal(str)
    signal_progress = Signal(int)
    signal_finished = Signal(bool, str)

    def __init__(self, prompt: str, output_dir: str | Path, model: str = "", parent=None) -> None:
        super().__init__(parent)
        self.prompt = prompt
        self.output_dir = Path(output_dir)
        self.model = model or ""
        self._process: subprocess.Popen | None = None
        self._stopped = False

    def stop(self) -> None:
        self._stopped = True
        process = self._process
        if process is None or process.poll() is not None:
            return
        if sys.platform == "win32":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(process.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=CREATE_NO_WINDOW,
                check=False,
            )
        else:
            process.kill()

    def run(self) -> None:
        agy = find_agy()
        if not agy:
            self.signal_log.emit("Không tìm thấy agy.exe trên PATH hoặc trong %LOCALAPPDATA%\\agy.")
            self.signal_finished.emit(False, "Không tìm thấy agy.exe")
            return

        runtime = writable_dir() / ".runtime"
        runtime.mkdir(parents=True, exist_ok=True)
        prompt_path = runtime / "lenh_hien_tai.md"
        prompt_path.write_text(self.prompt, encoding="utf-8")
        started = prompt_path.stat().st_mtime
        work = writable_dir()

        # Prompt nghiệp vụ nằm trong tệp UTF-8 vì lệnh -p có trần độ dài của Windows.
        # Câu kích hoạt tiếng Anh không dấu để Windows CLI không làm hỏng ký tự.
        # --disable-slash-commands tránh kích hoạt skill khi quy chuẩn chứa dấu gạch chéo.
        command = build_agy_command(agy, prompt_path, self.model)
        self.signal_log.emit(f"Khởi chạy: {agy}")
        if self.model.strip():
            self.signal_log.emit(f"Mô hình: {self.model.strip()}")
        self.signal_log.emit(f"Thư mục làm việc: {work}")
        self.signal_progress.emit(3)

        try:
            self._process = subprocess.Popen(
                command,
                cwd=str(work),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
        except OSError as exc:
            self.signal_log.emit(f"Không chạy được agy.exe: {exc}")
            self.signal_finished.emit(False, str(exc))
            return

        watch = self._read_stream(self._process.stdout)
        captured = watch.captured

        code = self._process.wait()
        if self._stopped:
            self.signal_log.emit("Đã dừng tiến trình theo yêu cầu.")
            self.signal_finished.emit(False, "Đã dừng")
            return

        result = captured
        result_path = Path(result) if result else None
        if result_path is None or not result_path.exists():
            newest = _newest_file(self.output_dir, started)
            if newest is not None:
                result = str(newest)
        if code == 0:
            self.signal_progress.emit(100)
            message = result or str(self.output_dir)
            self.signal_log.emit(f"Hoàn thành. Kết quả: {message}")
            self.signal_finished.emit(True, message)
            return
        self.signal_log.emit(f"agy thoát với mã {code}.")
        self.signal_finished.emit(False, result or f"agy thoát với mã {code}")

    def _read_stream(self, stream) -> StreamWatch:
        """Đọc stdout theo dòng. Im lặng vài giây thì báo AI vẫn đang suy luận."""
        watch = StreamWatch()
        if stream is None:
            return watch
        pending: queue.Queue[str | None] = queue.Queue()

        def pump() -> None:
            try:
                for raw in stream:
                    pending.put(raw)
            finally:
                pending.put(None)

        threading.Thread(target=pump, name="agy-stdout", daemon=True).start()
        announced = watch.progress
        emitted = 0
        quiet_since = time.monotonic()
        while not self._stopped:
            try:
                raw = pending.get(timeout=HEARTBEAT_SECONDS)
            except queue.Empty:
                waited = int(time.monotonic() - quiet_since)
                self.signal_log.emit(f"AI đang suy luận… ({waited}s)")
                if watch.progress < 90:
                    watch.progress += 1
                    announced = watch.progress
                    self.signal_progress.emit(watch.progress)
                continue
            if raw is None:
                break
            quiet_since = time.monotonic()
            interpret_stream_line(raw, watch)
            emitted, announced = self._emit_watch(watch, emitted, announced)
        emitted, announced = self._emit_watch(watch, emitted, announced)
        return watch

    def _emit_watch(self, watch: StreamWatch, emitted: int, announced: int) -> tuple[int, int]:
        while emitted < len(watch.logs):
            self.signal_log.emit(watch.logs[emitted])
            emitted += 1
        if watch.progress != announced:
            announced = watch.progress
            self.signal_progress.emit(watch.progress)
        return emitted, announced
