import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""

authority_address = "0x80fa483469e4Dfb8C947f107EC18bf78C7D86871"
authority_key = "0x90283aefbe11590dcb12fe20a933834d61001b46520353df79ac7120cb911334"
"""
plasma_config = dict(
    ROOT_CHAIN_CONTRACT_ADDRESS='0x42aF249d7e61E304369A485583a093Bf1C9D30bC',
    AUTHORITY=b'\xe6[1\x8b\x9d\xec\xf5\x04\xd1\xcbn\xa5\xc3g\xcaez\x07\r\xb1',
    AUTHORITY_KEY=b'\x1ew\x1d\xa3\xa1\xdc\xae\x0f\xd7z\x94,\xc8\x16\xfdk\x9bL\xca\x97"\x0f\x8e\xa6\xc6x*\x84\x87\x14\x12\x9d',
)


db_config = {
    'type': 'leveldb' # | 'memory' # (required)
    # 'path': '' (optional, if nor specific set, would have default path)
}
"""
db_config = {
    'type': 'memory'
}
"""