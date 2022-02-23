import os
import glob
import pandas as pd
import json
from loguru import logger


class Process:
    '''
    Class that performs extraction of data from files, get reports data by transformations
    and load into a reports files
    '''

    def __init__(self):
        self.__data = pd.DataFrame()
        logger.info('starting...')

    @logger.catch()
    def extraction(self, folder):
        '''
        Function that extract data from a folder
        :param str folder: folder that contains data files
        '''
        path = os.getcwd()
        path = path + '/' + folder
        files = glob.glob(os.path.join(path, "*.json"))
        logger.info('extracting {} files...'.format(len(files)))
        for file in files:
            f = open(file)
            df_data = pd.json_normalize(json.load(f))
            df_data['season'] = file.replace('_json.json', '')\
                                    .replace(path, '')\
                                    .replace('/', '')\
                                    .replace('\\', '')
            frames = [self.__data, df_data]
            self.__data = pd.concat(frames)
        logger.info(f'extracted {len(self.__data)} rows...')

    @logger.catch()
    def get_position_table_by_season(self):
        '''
        Function that transforms the data to obtain a table of positions for each season
        '''
        logger.info('getting position table by season...')
        position_table = self.__data.loc[self.__data['Div'] == 'E0',
                                         ['season', 'HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG']]
        position_table['HomePoints'] = [3 if x == 'H' else 1 if x == 'D' else 0 for x in position_table.FTR]
        position_table_home = position_table.groupby(['season', 'HomeTeam'], as_index=False).sum()
        position_table_home = position_table_home.rename(columns={'HomeTeam': 'Team',
                                                                  'HomePoints': 'Points',
                                                                  'FTHG': 'Goals',
                                                                  'FTAG': 'GoalsConceded'})
        position_table.drop(columns=['HomePoints'], inplace=True)
        position_table['AwayPoints'] = [3 if x == 'A' else 1 if x == 'D' else 0 for x in position_table.FTR]
        position_table_away = position_table.groupby(['season', 'AwayTeam'], as_index=False).sum()
        position_table_away = position_table_away.rename(columns={'AwayTeam': 'Team',
                                                                  'AwayPoints': 'Points',
                                                                  'FTHG': 'GoalsConceded',
                                                                  'FTAG': 'Goals'})
        frames = [position_table_home, position_table_away]
        position_table_by_season = pd.concat(frames)
        position_table_by_season = position_table_by_season.groupby(['season', 'Team'], as_index=False).sum()
        position_table_by_season['GoalDifference'] = position_table_by_season['Goals'] \
            - position_table_by_season['GoalsConceded']
        position_table_by_season.sort_values(by=['Points', 'GoalDifference'], ascending=False, inplace=True)
        logger.info('report ready...')
        return position_table_by_season

    @logger.catch()
    def get_most_scored_team(self):
        '''
        Function that transforms the data to obtain the most scored team for each season
        '''
        logger.info('getting most scored team by season...')
        scored_table = self.__data.loc[self.__data['Div'] == 'E0',
                                       ['season', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
        scored_table_home = scored_table.groupby(['season', 'HomeTeam'], as_index=False).sum()
        scored_table_home = scored_table_home.rename(columns={'HomeTeam': 'Team',
                                                              'FTAG': 'GoalsConceded',
                                                              'FTHG': 'Goals'})
        scored_table_away = scored_table.groupby(['season', 'AwayTeam'], as_index=False).sum()
        scored_table_away = scored_table_away.rename(columns={'AwayTeam': 'Team',
                                                              'FTHG': 'GoalsConceded',
                                                              'FTAG': 'Goals'})
        frames = [scored_table_home, scored_table_away]
        scored_table_by_season = pd.concat(frames)
        scored_table_by_season.drop(columns=['Goals'], inplace=True)

        scored_table_by_season = scored_table_by_season.groupby(['season', 'Team'], as_index=False).sum()
        max = scored_table_by_season.groupby('season')['GoalsConceded'].max()
        scored_table_by_season['max'] = scored_table_by_season['season'].map(max)

        scored_table_by_season = scored_table_by_season.loc[
            scored_table_by_season['GoalsConceded'] == scored_table_by_season['max']]
        scored_table_by_season.drop(columns=['max'], inplace=True)

        logger.info('report ready...')
        return scored_table_by_season

    @logger.catch()
    def get_best_ratio_by_season(self):
        '''
        Function that transforms the data to obtain the team with
        the best ratio of shots on goal finishing in goal per season
        '''
        logger.info('getting team with best ratio goals by season...')
        ratio_table_home = self.__data.loc[self.__data['Div'] == 'E0',
                                           ['season', 'HomeTeam', 'HST', 'FTHG']]
        ratio_group_home = ratio_table_home.groupby(['season', 'HomeTeam'], as_index=False).sum()
        ratio_group_home = ratio_group_home.rename(columns={'HomeTeam': 'Team',
                                                            'HST': 'ShotsTarget',
                                                            'FTHG': 'Goals'})
        ratio_table_away = self.__data.loc[self.__data['Div'] == 'E0',
                                           ['season', 'AwayTeam', 'AST', 'FTAG']]
        ratio_group_away = ratio_table_away.groupby(['season', 'AwayTeam'], as_index=False).sum()
        ratio_group_away = ratio_group_away.rename(columns={'AwayTeam': 'Team',
                                                            'AST': 'ShotsTarget',
                                                            'FTAG': 'Goals'})
        frames = [ratio_group_home, ratio_group_away]
        ratio_table_by_season = pd.concat(frames)
        ratio_group_by_season = ratio_table_by_season.groupby(['season', 'Team'], as_index=False).sum()
        ratio_group_by_season['ratio'] = ratio_group_by_season.Goals / ratio_group_by_season.ShotsTarget
        max = ratio_group_by_season.groupby('season')['ratio'].max()
        ratio_group_by_season['max'] = ratio_group_by_season['season'].map(max)

        ratio_group_by_season = ratio_group_by_season.loc[
            ratio_group_by_season['ratio'] == ratio_group_by_season['max']]
        ratio_group_by_season.drop(columns=['max'], inplace=True)
        logger.info('report ready...')
        return ratio_group_by_season

    @logger.catch()
    def load_data(self, data, folder, report):
        path = os.getcwd()
        data.to_csv('{0}/{1}/{2}.csv'.format(str(path), folder, report), index=False)
        logger.info('report {} loaded...'.format(report))
