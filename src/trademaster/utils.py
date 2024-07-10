from typing import Dict, List, Optional, Union


def token_lookup(
    ticker: str,
    instrument_list: List[Dict[str, Union[str, int]]],
    exchange: str = 'NSE',
) -> Optional[int]:
    """Lookup the token for a given ticker."""
    for instrument in instrument_list:
        if (
            instrument['name'] == ticker
            and instrument['exch_seg'] == exchange
            and instrument['symbol'].split('-')[-1] == 'EQ'
        ):
            return instrument['token']
    return None

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'