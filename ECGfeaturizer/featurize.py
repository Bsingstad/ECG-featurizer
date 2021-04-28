import numpy as np
import wfdb
import neurokit2 as nk
#import plotly.graph_objects as go
import pandas as pd
import os
from scipy.io import loadmat

class get_features:

    def __init__(self, r_peak = True, r_int = True, p_peak = True, p_int = True, t_peak = True, t_int = True, q_peak = True, q_int= True, s_peak = True, s_int = True, qrs_dur= True, qt_dur = True, pr_dur = True):
        #elf.X_matrix = None
        self.rpeak_int = r_int
        self.ppeak_int = p_int
        self.tpeak_int = t_int
        self.qpeak_int = q_int
        self.speak_int = s_int
        
        
        
        self.rpeak_amp = r_peak
        self.ppeak_amp = p_peak
        self.tpeak_amp = t_peak
        self.qpeak_amp = q_peak
        self.speak_amp = s_peak
        
        self.qrs_duration = qrs_dur
        self.qt_duration = qt_dur
        self.pr_duration = pr_dur

        self.files_for_manual_annotation = []
        self.labels_for_manual_annotation = None
        
    def featurize_ecg(self, recording, sample_freq):
        """
        Automatically derives features from ECG-files (only .dat files for now)
        Args:
            features (numpy array of str): an array of ECG-filenames in directory
            labels (numpy array): an array of labels/diagnosis
            directory (str): path to the features
            demographical_data (DataFrame): A DataFrame containing feature name, age and gender

        Returns:
            features_out (DataFrame): A DataFrame with features for all ECG-records
        """

        
        def interval_calc(q_peaks, s_peaks, sample_freq):
            if len(q_peaks) != len(s_peaks):
                for i,j in enumerate(q_peaks):
                    if j > s_peaks[0]:
                        if j == 0:
                            start_q = 0
                        else:
                            start_q = i-1
                        q_peaks=q_peaks[start_q:]
                        break   
                if len(q_peaks) != len(s_peaks):
                    if len(q_peaks[start_q:]) > len(s_peaks):
                        q_end = len(q_peaks)-len(s_peaks)
                        q_peaks = q_peaks[:-q_end]
                    else:
                        s_peaks = s_peaks[:-(len(s_peaks)-len(q_peaks))]
                rmssd_qrs = round(rmssd_calc((s_peaks-q_peaks)/sample_freq),5)
                mean_qrs = np.nan
                std_qrs = np.nan
            else:
                rmssd_qrs = round(rmssd_calc((s_peaks-q_peaks)/sample_freq),5)
                mean_qrs = round((s_peaks-q_peaks).mean(),5)
                std_qrs = round((s_peaks-q_peaks).std(),5)

            return np.array([rmssd_qrs,mean_qrs,std_qrs])
        
        def interval_calc_simple(first_peak, second_peak, sample_freq):
            try:
                mean_interval = round((second_peak-first_peak).mean(),5)
            except:
                mean_interval = float("NaN")
            try:
                std_interval = round((second_peak-first_peak).std(),5)
            except:
                std_interval = float("NaN")
            return mean_interval, std_interval
        
        feature_list = []
        feature_name = []
        
        temp_data = nk.ecg_process(recording,sample_freq)[0]
        r_peaks = np.where(temp_data['ECG_R_Peaks']==1)[0]
        p_peaks = np.where(temp_data['ECG_P_Peaks']==1)[0]
        q_peaks = np.where(temp_data['ECG_Q_Peaks']==1)[0]
        s_peaks = np.where(temp_data['ECG_S_Peaks']==1)[0]
        t_peaks = np.where(temp_data['ECG_T_Peaks']==1)[0]
        p_onset = np.where(temp_data['ECG_P_Onsets']==1)[0]
        t_offset = np.where(temp_data['ECG_T_Offsets']==1)[0]
        
        if self.rpeak_int == True:
            feature_list.append((np.diff(r_peaks)/sample_freq).mean())
            feature_list.append((np.diff(r_peaks)/sample_freq).std())
            feature_name.append("mean_rr_interval")
            feature_name.append("sd_rr_interval")
        if self.rpeak_amp == True:
            feature_list.append(recording[r_peaks].mean())
            feature_list.append(recording[r_peaks].std())
            feature_name.append("mean_r_peak")
            feature_name.append("sd_r_peak")
        if self.ppeak_int == True:
            feature_list.append((np.diff(p_peaks)/sample_freq).mean())
            feature_list.append((np.diff(p_peaks)/sample_freq).std())
            feature_name.append("mean_pp_interval")
            feature_name.append("sd_pp_interval")          
        if self.ppeak_amp == True:
            feature_list.append(recording[p_peaks].mean())
            feature_list.append(recording[p_peaks].std())
            feature_name.append("mean_p_peak")
            feature_name.append("sd_p_peak")
        if self.tpeak_int == True:
            feature_list.append((np.diff(t_peaks)/sample_freq).mean())
            feature_list.append((np.diff(t_peaks)/sample_freq).std())
            feature_name.append("mean_tt_interval")
            feature_name.append("sd_tt_interval")          
        if self.tpeak_amp == True:
            feature_list.append(recording[t_peaks].mean())
            feature_list.append(recording[t_peaks].std())
            feature_name.append("mean_t_peak")
            feature_name.append("sd_t_peak")
        if self.qpeak_int == True:
            feature_list.append((np.diff(q_peaks)/sample_freq).mean())
            feature_list.append((np.diff(q_peaks)/sample_freq).std())
            feature_name.append("mean_qq_interval")
            feature_name.append("sd_qq_interval")          
        if self.qpeak_amp == True:
            feature_list.append(recording[q_peaks].mean())
            feature_list.append(recording[q_peaks].std())
            feature_name.append("mean_q_peak")
            feature_name.append("sd_q_peak")
        if self.speak_int == True:
            feature_list.append((np.diff(s_peaks)/sample_freq).mean())
            feature_list.append((np.diff(s_peaks)/sample_freq).std())
            feature_name.append("mean_ss_interval")
            feature_name.append("sd_ss_interval")          
        if self.speak_amp == True:
            feature_list.append(recording[s_peaks].mean())
            feature_list.append(recording[s_peaks].std())
            feature_name.append("mean_s_peak")
            feature_name.append("sd_s_peak")
        if self.qrs_duration == True:
            qrs_mean, qrs_std = interval_calc_simple(q_peaks,s_peaks,sample_freq)
            feature_list.append(qrs_mean)
            feature_list.append(qrs_std)
            feature_name.append("qrs_mean")
            feature_name.append("qrs_std")
        if self.qt_duration == True:
            qt_mean, qt_std = interval_calc_simple(q_peaks,t_peaks,sample_freq)
            feature_list.append(qt_mean)
            feature_list.append(qt_std)
            feature_name.append("qt_mean")
            feature_name.append("qt_std")
        if self.pr_duration == True:
            pr_mean, pr_std = interval_calc_simple(p_peaks,r_peaks,sample_freq)
            feature_list.append(pr_mean)
            feature_list.append(pr_std)
            feature_name.append("pr_mean")
            feature_name.append("pr_std")
            
        feature_list = np.asarray(feature_list)
        feature_name = np.asarray(feature_name)
            
        return feature_list,feature_name
            
            
        
            
            

