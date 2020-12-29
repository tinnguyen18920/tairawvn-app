# class DownloadImageException(Exception):
#     """When response is not ok from an image"""



response = {
    "invalid_url": {"status": "error", "msg": "Invalid URL"},
    "request_url_error": {"status": "error", "msg": "Can not download webpage"},
    "need_buy": {"status": "error", "msg": "need buy episode"},
    "not_found": {"status": "error", "msg": "Chap not found"},
    "site_changed": {"status": "error", "msg": "Changed"},
    "not_logged_in": {"status": "error", "msg": "Not logged in"}
}