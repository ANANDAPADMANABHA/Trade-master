from typing import List, Dict, Union, Optional

    
def token_lookup(ticker: str, instrument_list: List[Dict[str, Union[str, int]]], exchange: str = "NSE") -> Optional[int]:
        """Lookup the token for a given ticker."""
        for instrument in instrument_list:
            if (instrument["name"] == ticker and
                instrument["exch_seg"] == exchange and
                    instrument["symbol"].split('-')[-1] == "EQ"):
                return instrument["token"]
        return None
    