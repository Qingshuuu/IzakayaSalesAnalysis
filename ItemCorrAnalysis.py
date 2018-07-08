import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

from Common.Logic.Preprocess import Preprocess
from Common.Logic.Postprocess import Postprocess
from Common.Setting.PreprocessSetting import PreprocessSetting


class ItemCorrAnalysisSetting(object):
    CORR_LIMIT = 0.5

# 商品間の相関係数算出クラス
class ItemCorrAnalysis:

    def __init__(self):
        self.preproc_s = PreprocessSetting()
        self.aca_s = ItemCorrAnalysisSetting()
        self.preproc = Preprocess()
        self.postproc = Postprocess()


    def execute(self):
        preproc_csv_path = self._preprocess()
        # preproc_csv_path = ''
        self.df_preproc = self._get_preproc_data(preproc_csv_path)
        corr = self._calc_correlation(self.df_preproc)
        print(corr)
        self._plot_corr(corr)
        
        
        # self._create_prediction_model()
        # self._postprocess()


    def _preprocess(self):
        df_src = self.preproc.fetch_csv_data_and_convert_format_to_df(self.preproc_s.PROCESSED_DATA_DIR,self.preproc_s.DATA_FILES_TO_FETCH)
        df_src = self.preproc.divide_col(df_src, self.preproc_s.DIVIDE_NECESSARY_COLS)
        # df_src = self.preproc.grouping(df_src, self.preproc_s.GROUPING_KEY_DOW, self.preproc_s.GROUPING_WAY)
        df_src = self.preproc.tanspose_cols_and_rows(df_src, self.preproc_s.GROUPING_KEY_DAY_BILL_ORDER,
                                                           self.preproc_s.TGT_TRANPOSE_C_AND_R_COL,
                                                           self.preproc_s.TMP_COLS)

        df_src = self.preproc.change_label_name(df_src)
        preproc_csv_file_name = self.preproc.create_proc_data_csv(df_src, self.preproc_s.PROCESSED_DATA_DIR,
                                                                  self.preproc_s.TGT_STORE,
                                                                  self.preproc_s.TGT_PERIOD_FLOOR,
                                                                  self.preproc_s.TGT_PERIOD_TOP,
                                                                  '_'+self.preproc_s.GROUPING_FILE_MEMO)

        return preproc_csv_file_name

    def _get_preproc_data(self, csv_file_name):
        return pd.read_csv(self.preproc_s.PROCESSED_DATA_DIR + csv_file_name, encoding = 'cp932')

    # for debug
    def _calc_correlation(self, df_preproc):
        return df_preproc.corr(method='pearson')

    def _plot_corr(self,df_corr):
        df_corr = df_corr[(df_corr >= self.aca_s.CORR_LIMIT) | (df_corr <= -self.aca_s.CORR_LIMIT)]
        df_corr.replace(1,np.nan,inplace=True)
        df_corr.dropna(how='all',inplace=True)
        df_corr.dropna(how='all',axis=1,inplace=True)
        sns.heatmap(df_corr,vmin=-1.0,vmax=1.0,center=0,
                    annot=True,  # True:格子の中に値を表示
                    fmt='.1f',
                    xticklabels=df_corr.columns.values,
                    yticklabels=df_corr.columns.values
                    )
        plt.show()


if __name__ == '__main__':
    ica = ItemCorrAnalysis()
    ica.execute()