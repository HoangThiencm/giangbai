# PATCH: Đã gộp vào backend/thitructuyen.py (cuối file).
# Triển khai lên HuggingFace Space hoangthiencm/giangbai:
#   1. Mở https://huggingface.co/spaces/hoangthiencm/giangbai → tab Files → thitructuyen.py
#   2. Thay nội dung bằng file backend/thitructuyen.py trong repo này (hoặc chỉ thêm đoạn dưới vào cuối file HF)
#   3. Commit → Space tự restart
#
# API mới:
#   DELETE /api/exam/result/{id}           — xóa một lượt thi
#   POST   /api/exam/results/delete-batch  — body: { "ids": [1, 2, 3] }

class DeleteResultsBatchRequest(BaseModel):
    ids: List[int]


@router.delete("/result/{result_id}")
def delete_result(result_id: int):
    if not supabase:
        raise HTTPException(500, "DB Error")
    check = supabase.table("submissions").select("id").eq("id", result_id).execute()
    if not check.data:
        raise HTTPException(404, "Không tìm thấy kết quả")
    supabase.table("submissions").delete().eq("id", result_id).execute()
    return {"status": "ok", "message": "Đã xóa kết quả", "id": result_id}


@router.post("/results/delete-batch")
def delete_results_batch(body: DeleteResultsBatchRequest):
    if not supabase:
        raise HTTPException(500, "DB Error")
    ids = [int(i) for i in (body.ids or []) if i is not None]
    if not ids:
        raise HTTPException(400, "Thiếu danh sách id")
    supabase.table("submissions").delete().in_("id", ids).execute()
    return {"status": "ok", "deleted": len(ids)}