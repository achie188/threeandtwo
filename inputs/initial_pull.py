import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/Personal/threeandtwo')

from pull_sportsdb import get_all_results
from outputs.to_gsheets import send_to_gsheet, clear_gsheet

league_id = '4424'

#Get all past seasons in those leagues
all_results = get_all_results(league_id)

#Send to gsheets
clear_gsheet("threeandTwo Baseball Data", "All Results")

send_to_gsheet(all_results, "threeandTwo Baseball Data", "All Results")

