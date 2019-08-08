kernel_space = [None] * 512
app_space = [None] * 1024
pointers = [None] * 2048
storage = [None] * 10240

memory = kernel_space + app_space + pointers + storage

def load_kernel():
    pass

def fetch_app(app_id):
    pass

def fetch_blocks(block_range):
    pass

def store_app(app_id):
    pass

def store_blocks(source_block_range,target_block_range):
    pass
