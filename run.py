from src.process import Process

source_folder = 'data'
sink_folder = 'reports'
if __name__ == "__main__":
    process = Process()
    process.extraction(source_folder)
    position_table = process.get_position_table_by_season()
    process.load_data(data=position_table, folder=sink_folder, report='position_table_by_season')
    scored_table = process.get_most_scored_team()
    process.load_data(data=scored_table, folder=sink_folder, report='most_scored_team_by_season')
    ratio_table = process.get_best_ratio_by_season()
    process.load_data(data=ratio_table, folder=sink_folder, report='best_ratio_team_by_season')
