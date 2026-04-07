import threading


lock            = threading.Lock()

latest_qr       : str   = ""
latest_time     : str   = ""
has_new_qr      : bool  = False
scan_count      : int   = 0

last_qr         : str   = ""
last_qr_time    : float = 0.0
