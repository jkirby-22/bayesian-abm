import pstats
from pstats import SortKey
p = pstats.Stats('profile_results_top_level')
p.sort_stats(SortKey.CUMULATIVE).print_stats(10)