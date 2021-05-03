import numpy as np
import wfdb
import neurokit2 as nk
#import plotly.graph_objects as go
import pandas as pd
import os
from scipy.io import loadmat
from wfdb import processing

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
            R-peaks
            P-peaks
            T-peaks
        
            features (numpy array of str): an array of ECG-filenames in directory
            labels (numpy array): an array of labels/diagnosis
            directory (str): path to the features
            demographical_data (DataFrame): A DataFrame containing feature name, age and gender

        Returns:
            features_out (DataFrame): A DataFrame with features for all ECG-records
        """

        
     
        
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
        try:
            temp_data = nk.ecg_process(recording,sample_freq)[0]
            r_peaks = np.where(temp_data['ECG_R_Peaks']==1)[0]
            p_peaks = np.where(temp_data['ECG_P_Peaks']==1)[0]
            q_peaks = np.where(temp_data['ECG_Q_Peaks']==1)[0]
            s_peaks = np.where(temp_data['ECG_S_Peaks']==1)[0]
            t_peaks = np.where(temp_data['ECG_T_Peaks']==1)[0]
            p_onset = np.where(temp_data['ECG_P_Onsets']==1)[0]
            t_offset = np.where(temp_data['ECG_T_Offsets']==1)[0]

            analysis = True
        except:
            analysis = False
            r_peaks = float("nan")

        
        if self.rpeak_int == True:
            feature_name.append("mean_rr_interval")
            feature_name.append("sd_rr_interval")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append((np.diff(r_peaks)/sample_freq).mean())
                feature_list.append((np.diff(r_peaks)/sample_freq).std())
            

        if self.rpeak_amp == True:
            feature_name.append("mean_r_peak")
            feature_name.append("sd_r_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                # Dont use cleaned signal
                feature_list.append(recording[r_peaks].mean())
                feature_list.append(recording[r_peaks].std())

        if self.ppeak_int == True:
            feature_name.append("mean_pp_interval")
            feature_name.append("sd_pp_interval") 
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append((np.diff(p_peaks)/sample_freq).mean())
                feature_list.append((np.diff(p_peaks)/sample_freq).std())
         
        if self.ppeak_amp == True:
            feature_name.append("mean_p_peak")
            feature_name.append("sd_p_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append(temp_data['ECG_Clean'][p_peaks].mean())
                feature_list.append(temp_data['ECG_Clean'][p_peaks].std())

        if self.tpeak_int == True:
            feature_name.append("mean_tt_interval")
            feature_name.append("sd_tt_interval")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append((np.diff(t_peaks)/sample_freq).mean())
                feature_list.append((np.diff(t_peaks)/sample_freq).std())
         
        if self.tpeak_amp == True:
            feature_name.append("mean_t_peak")
            feature_name.append("sd_t_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                 
                feature_list.append(temp_data['ECG_Clean'][t_peaks].mean())
                feature_list.append(temp_data['ECG_Clean'][t_peaks].std())

        if self.qpeak_int == True:
            feature_name.append("mean_qq_interval")
            feature_name.append("sd_qq_interval") 
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True: 
                feature_list.append((np.diff(q_peaks)/sample_freq).mean())
                feature_list.append((np.diff(q_peaks)/sample_freq).std())
         
        if self.qpeak_amp == True:
            feature_name.append("mean_q_peak")
            feature_name.append("sd_q_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                         
                feature_list.append(temp_data['ECG_Clean'][q_peaks].mean())
                feature_list.append(temp_data['ECG_Clean'][q_peaks].std())

        if self.speak_int == True:
            feature_name.append("mean_q_peak")
            feature_name.append("sd_q_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                        
                feature_list.append((np.diff(s_peaks)/sample_freq).mean())
                feature_list.append((np.diff(s_peaks)/sample_freq).std())
                                    
        if self.speak_amp == True:
            feature_name.append("mean_s_peak")
            feature_name.append("sd_s_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                        
                feature_list.append(temp_data['ECG_Clean'][s_peaks].mean())
                feature_list.append(temp_data['ECG_Clean'][s_peaks].std())

        if self.qrs_duration == True:
            feature_name.append("qrs_mean")
            feature_name.append("qrs_std")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan")) 
            elif analysis == True:                         
                qrs_mean, qrs_std = interval_calc_simple(q_peaks,s_peaks,sample_freq)
                feature_list.append(qrs_mean)
                feature_list.append(qrs_std)
                                    
        if self.qt_duration == True:
            feature_name.append("qt_mean")
            feature_name.append("qt_std")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                qt_mean, qt_std = interval_calc_simple(q_peaks,t_peaks,sample_freq)
                feature_list.append(qt_mean)
                feature_list.append(qt_std)

        if self.pr_duration == True:
            feature_name.append("pr_mean")
            feature_name.append("pr_std")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                pr_mean, pr_std = interval_calc_simple(p_peaks,r_peaks,sample_freq)
                feature_list.append(pr_mean)
                feature_list.append(pr_std)

            
        feature_list = np.asarray(feature_list)
        feature_name = np.asarray(feature_name)
         
        return feature_list,feature_name, [p_peaks,q_peaks,r_peaks,s_peaks,t_peaks]
    
    def corr_and_featurize_ecg(self, recording, sample_freq, r_peaks, s_peaks, q_peaks, p_peaks, t_peaks):
        """
        Automatically derives features from ECG-files (only .dat files for now)
        Args:
            R-peaks
            P-peaks
            T-peaks
        
            features (numpy array of str): an array of ECG-filenames in directory
            labels (numpy array): an array of labels/diagnosis
            directory (str): path to the features
            demographical_data (DataFrame): A DataFrame containing feature name, age and gender

        Returns:
            features_out (DataFrame): A DataFrame with features for all ECG-records
        """

        

        
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
        
        if len(r_peaks) and len(q_peaks) and len(s_peaks) and len(p_peaks) and len(t_peaks) < 3:
            try:
                temp_data = nk.ecg_process(recording,sample_freq)[0]
                r_peaks = np.where(temp_data['ECG_R_Peaks']==1)[0]
                p_peaks = np.where(temp_data['ECG_P_Peaks']==1)[0]
                q_peaks = np.where(temp_data['ECG_Q_Peaks']==1)[0]
                s_peaks = np.where(temp_data['ECG_S_Peaks']==1)[0]
                t_peaks = np.where(temp_data['ECG_T_Peaks']==1)[0]
                p_onset = np.where(temp_data['ECG_P_Onsets']==1)[0]
                t_offset = np.where(temp_data['ECG_T_Offsets']==1)[0]

                analysis = True
            except:
                analysis = False
                r_peaks = float("nan")
        
        else:
            analysis = True
            clean_rec = nk.ecg_clean(recording)
            
            r_peaks = processing.peaks.correct_peaks(clean_rec, r_peaks, search_radius=25, 
                                                     smooth_window_size=7, peak_dir='compare')
            q_peaks = processing.peaks.correct_peaks(clean_rec, q_peaks, search_radius=25, 
                                                      smooth_window_size=7, peak_dir='compare')
            s_peaks = processing.peaks.correct_peaks(clean_rec, s_peaks, search_radius=25, 
                                                          smooth_window_size=7, peak_dir='compare')
            t_peaks = processing.peaks.correct_peaks(clean_rec, t_peaks, search_radius=25, 
                                                              smooth_window_size=7, peak_dir='compare')
            p_peaks = processing.peaks.correct_peaks(clean_rec, p_peaks, search_radius=25, 
                                                              smooth_window_size=7, peak_dir='compare')
            

        
        if self.rpeak_int == True:
            feature_name.append("mean_rr_interval")
            feature_name.append("sd_rr_interval")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append((np.diff(r_peaks)/sample_freq).mean())
                feature_list.append((np.diff(r_peaks)/sample_freq).std())
            

        if self.rpeak_amp == True:
            feature_name.append("mean_r_peak")
            feature_name.append("sd_r_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append(recording[r_peaks].mean())
                feature_list.append(recording[r_peaks].std())

        if self.ppeak_int == True:
            feature_name.append("mean_pp_interval")
            feature_name.append("sd_pp_interval") 
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append((np.diff(p_peaks)/sample_freq).mean())
                feature_list.append((np.diff(p_peaks)/sample_freq).std())
         
        if self.ppeak_amp == True:
            feature_name.append("mean_p_peak")
            feature_name.append("sd_p_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append(clean_rec[p_peaks].mean())
                feature_list.append(clean_rec[p_peaks].std())

        if self.tpeak_int == True:
            feature_name.append("mean_tt_interval")
            feature_name.append("sd_tt_interval")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                feature_list.append((np.diff(t_peaks)/sample_freq).mean())
                feature_list.append((np.diff(t_peaks)/sample_freq).std())
         
        if self.tpeak_amp == True:
            feature_name.append("mean_t_peak")
            feature_name.append("sd_t_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                 
                feature_list.append(clean_rec[t_peaks].mean())
                feature_list.append(clean_rec[t_peaks].std())

        if self.qpeak_int == True:
            feature_name.append("mean_qq_interval")
            feature_name.append("sd_qq_interval") 
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True: 
                feature_list.append((np.diff(q_peaks)/sample_freq).mean())
                feature_list.append((np.diff(q_peaks)/sample_freq).std())
         
        if self.qpeak_amp == True:
            feature_name.append("mean_q_peak")
            feature_name.append("sd_q_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                         
                feature_list.append(clean_rec[q_peaks].mean())
                feature_list.append(clean_rec[q_peaks].std())

        if self.speak_int == True:
            feature_name.append("mean_q_peak")
            feature_name.append("sd_q_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                        
                feature_list.append((np.diff(s_peaks)/sample_freq).mean())
                feature_list.append((np.diff(s_peaks)/sample_freq).std())
                                    
        if self.speak_amp == True:
            feature_name.append("mean_s_peak")
            feature_name.append("sd_s_peak")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:                        
                feature_list.append(clean_rec[s_peaks].mean())
                feature_list.append(clean_rec[s_peaks].std())

        if self.qrs_duration == True:
            feature_name.append("qrs_mean")
            feature_name.append("qrs_std")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan")) 
            elif analysis == True:                         
                qrs_mean, qrs_std = interval_calc_simple(q_peaks,s_peaks,sample_freq)
                feature_list.append(qrs_mean)
                feature_list.append(qrs_std)
                                    
        if self.qt_duration == True:
            feature_name.append("qt_mean")
            feature_name.append("qt_std")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                qt_mean, qt_std = interval_calc_simple(q_peaks,t_peaks,sample_freq)
                feature_list.append(qt_mean)
                feature_list.append(qt_std)

        if self.pr_duration == True:
            feature_name.append("pr_mean")
            feature_name.append("pr_std")
            if analysis == False:
                feature_list.append(float("nan"))
                feature_list.append(float("nan"))
            elif analysis == True:
                pr_mean, pr_std = interval_calc_simple(p_peaks,r_peaks,sample_freq)
                feature_list.append(pr_mean)
                feature_list.append(pr_std)

            
        feature_list = np.asarray(feature_list)
        feature_name = np.asarray(feature_name)
         
        return feature_list,feature_name