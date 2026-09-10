def process_rikkeimart_order(item_status, customer_response):
    """
    Mô phỏng luồng xử lý đơn hàng RikkeiMart.

    Quy tắc:
    - IN_STOCK: tiếp tục mua hàng bình thường.
    - OUT_OF_STOCK + ACCEPT: khách đồng ý sản phẩm thay thế.
    - OUT_OF_STOCK + REJECT: khách từ chối thay thế -> hủy an toàn.
    - OUT_OF_STOCK + TIMEOUT/không phản hồi: timeout 3 phút
      -> tự động xử lý an toàn để giải phóng tài xế.
    - Không làm chương trình crash khi dữ liệu đầu vào không hợp lệ.
    """

    try:
        status = str(item_status).strip().upper()
        response = str(customer_response).strip().upper()

        if status not in {"IN_STOCK", "OUT_OF_STOCK"}:
            return {
                "status": "ERROR",
                "message": "Trạng thái hàng hóa không hợp lệ."
            }

        if status == "IN_STOCK":
            return {
                "status": "CONTINUE",
                "message": "Sản phẩm còn hàng, tài xế tiếp tục mua hàng."
            }

        # Đến đây nghĩa là sản phẩm đã hết hàng.
        if response in {"ACCEPT", "YES", "APPROVE"}:
            return {
                "status": "SUBSTITUTED",
                "message": (
                    "Khách hàng đồng ý sản phẩm thay thế tương đương. "
                    "Tài xế tiếp tục mua sản phẩm thay thế."
                )
            }

        if response in {"REJECT", "NO", "CANCEL"}:
            return {
                "status": "CANCELLED",
                "message": (
                    "Khách hàng không đồng ý thay thế. "
                    "Đơn được hủy an toàn."
                )
            }

        # NONE, TIMEOUT, EMPTY hoặc phản hồi không xác định
        # được coi là không có phản hồi trong 3 phút.
        return {
            "status": "TIMEOUT_3_MINUTES",
            "message": (
                "Khách hàng không phản hồi trong 3 phút. "
                "Hệ thống tự động kết thúc nhánh thay thế an toàn "
                "để giải phóng tài xế."
            )
        }

    except Exception as exc:
        # Không để dữ liệu bất thường làm chương trình crash.
        return {
            "status": "ERROR",
            "message": f"Lỗi dữ liệu đầu vào: {exc}"
        }


# Ví dụ chạy thử
test_cases = [
    ("IN_STOCK", "NONE"),
    ("OUT_OF_STOCK", "ACCEPT"),
    ("OUT_OF_STOCK", "REJECT"),
    ("OUT_OF_STOCK", "TIMEOUT"),
    ("OUT_OF_STOCK", ""),
    ("INVALID", "ACCEPT"),
]

for item_status, customer_response in test_cases:
    result = process_rikkeimart_order(item_status, customer_response)
    print(
        f"Input: item_status={item_status!r}, "
        f"customer_response={customer_response!r}"
    )
    print("Output:", result)
    print("-" * 70)
