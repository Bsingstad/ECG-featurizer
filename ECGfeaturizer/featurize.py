import numpy as np
import wfdb
import neurokit2 as nk

class get_features:

    def __init__(self):
        #elf.X_matrix = None
        self.features_out = None
        self.files_for_manual_annotation = None
        self.labels_for_manual_annotation = None



    def featurizer(self, features , labels, directory, demographical_data):
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

        def _read_directory_data(ecg_file , directory):
            ecg_data, header_data =  wfdb.rdsamp(directory + ecg_file)
            samplefreq = header_data['fs']
            n_signal = header_data['n_sig']
            signal_len = header_data['sig_len']
            ecg_data = ecg_data.T
            return ecg_data, samplefreq, n_signal, signal_len

        def _read_demographical_data(demographical_data, ecg_file):
            try:
                age = int(demographical_data.iloc[np.where(demographical_data.filename_hr == "records500/00000/" + ecg_file)]['age'])
            except:
                age = -1

            try:
                gender = int(demographical_data.iloc[np.where(demographical_data.filename_hr == "records500/00000/" + ecg_file)]['sex'])
            except:
                gender = 2

            return age, gender
        
        def _find_R_peaks(ecg_data,samplefreq):
            _, rpeaks = nk.ecg_peaks(ecg_data[1], sampling_rate=samplefreq)
            r_peaks=rpeaks['ECG_R_Peaks']
            r_peaks = np.delete(r_peaks,np.where(np.isnan(r_peaks))[0]).astype(int)
            return r_peaks
        
        def _derive_R_features(r_peaks,ecg_data,samplefreq,_r_amp_leads,voltage_res=1):
            for i in range(ecg_data.shape[0]):
                _r_amp_leads[i] = (ecg_data[i][r_peaks]/voltage_res).mean()
            heartrate_r = (60/(np.diff(r_peaks)/samplefreq)) # not use
            heartrate_std = heartrate_r.std()
            heartrate_median = np.median(heartrate_r)
            heartrate_min = heartrate_r.min()
            heartrate_max = heartrate_r.max()
            mean_heartrate_r = (60/(np.diff(r_peaks)/samplefreq)).mean()
            rmssd = np.mean(np.square((60/(np.diff(r_peaks)/samplefreq))))
            r_amp_II_std = (ecg_data[1][r_peaks]/1).std()
            r_amp_II_min = (ecg_data[1][r_peaks]/1).min()
            r_amp_II_max = (ecg_data[1][r_peaks]/1).max()
            return _r_amp_leads, heartrate_r, heartrate_std, heartrate_median, heartrate_min, heartrate_max, mean_heartrate_r, rmssd, r_amp_II_std, r_amp_II_min, r_amp_II_max


        def _discrete_wavelet_trans(ecg_data,rpeaks,sample_freq):
            _, waves_dwt = nk.ecg_delineate(ecg_data[1], rpeaks, sampling_rate=sample_freq, method="dwt")
            p_offsets = waves_dwt['ECG_P_Offsets']
            p_offsets = np.delete(p_offsets,np.where(np.isnan(p_offsets))[0]).astype(int)
            p_onsets = waves_dwt['ECG_P_Onsets']
            p_onsets = np.delete(p_onsets,np.where(np.isnan(p_onsets))[0]).astype(int)
            p_peaks = waves_dwt['ECG_P_Peaks']
            p_peaks = np.delete(p_peaks,np.where(np.isnan(p_peaks))[0]).astype(int)
            t_peaks = waves_dwt['ECG_T_Peaks']
            t_peaks = np.delete(t_peaks,np.where(np.isnan(t_peaks))[0]).astype(int)
            t_offsets = waves_dwt['ECG_T_Offsets']
            t_offsets = np.delete(t_offsets,np.where(np.isnan(t_offsets))[0]).astype(int)
            t_onsets = waves_dwt['ECG_T_Onsets']
            t_onsets = np.delete(t_onsets,np.where(np.isnan(t_onsets))[0]).astype(int)
            return p_offsets, p_onsets, p_peaks, t_peaks, t_offsets, t_onsets

        def _other_peaks_detection(ecg_data,rpeaks,sampling_rate):
            _, waves_peak = nk.ecg_delineate(ecg_data[1], rpeaks, sampling_rate=sampling_rate)
            q_peaks = waves_peak['ECG_Q_Peaks']
            q_peaks = np.delete(q_peaks,np.where(np.isnan(q_peaks))[0]).astype(int) # not use
            s_peaks = waves_peak['ECG_S_Peaks']
            s_peaks = np.delete(s_peaks,np.where(np.isnan(s_peaks))[0]).astype(int) # not use
            return q_peaks, s_peaks


        voltage_res = 1
        feature_array = np.zeros((labels.shape[0],112))
        counter_all = 0
        counter_auto_annotated = 0
        labels_auto_annotated = []
        labels_not_annotated = []
        ecg_file_not_annotated = []
        for ecg_file in features:
            counter_all = counter_all + 1

            r_amp_leads = np.empty(12)
            p_amp_leads = np.empty(12)
            q_amp_leads = np.empty(12)
            s_amp_leads = np.empty(12)
            t_amp_leads = np.empty(12)

            ecgdata, fs, leads, sig_len = _read_directory_data(ecg_file,directory)

            age, gender = _read_demographical_data(demographical_data,ecg_file)
            try:
                r_peaks = _find_R_peaks(ecgdata,fs)
                r_amp_leads, heartrate_r, heartrate_std, heartrate_median, heartrate_min, heartrate_max, mean_heartrate_r, rmssd, r_amp_II_std, r_amp_II_min, r_amp_II_max =_derive_R_features(r_peaks, ecgdata, fs, r_amp_leads, voltage_res=voltage_res)
            except:
                print("Not able to get R-peak features")
                print("Future version will deal with this")
                labels_not_annotated.append(labels[counter_all])
                ecg_file_not_annotated.append(ecg_file)
                continue

            try:
                p_offsets, p_onsets, p_peaks, t_peaks, t_offsets, t_onsets = _discrete_wavelet_trans(ecgdata,r_peaks,fs)

                #-----------------------------------
                # P_offset features
                #-----------------------------------
                p_offset_rate= (60/(np.diff(p_offsets)/fs)) # not a feature
                p_offset_std = p_offset_rate.std()
                p_offset_median = np.median(p_offset_rate)
                p_offset_min = p_offset_rate.min()
                p_offset_max = p_offset_rate.max()
                mean_p_offset = p_offset_rate.mean()

                #-----------------------------------
                # P_onset features
                #-----------------------------------
                p_onsets_rate= (60/(np.diff(p_onsets)/fs)) # not a feature
                p_onsets_std = p_onsets_rate.std()
                p_onsets_median = np.median(p_onsets_rate)
                p_onsets_min = p_onsets_rate.min()
                p_onsets_max = p_onsets_rate.max()
                mean_p_onsets = p_onsets_rate.mean()

                #-----------------------------------
                # ECG_baseline
                #-----------------------------------
                ECG_baseline = (ecgdata[1][p_onsets] / voltage_res).mean() # use mean p onset as baseline

                #-----------------------------------
                # P_peak features
                #-----------------------------------
                p_peak_rate= (60/(np.diff(p_peaks)/fs)) # not a feature
                for i in range(ecgdata.shape[0]):
                    p_amp_leads[i] = (ecgdata[i][p_peaks]/voltage_res).mean()
                p_rate_std = p_peak_rate.std()
                p_rate_median = np.median(p_peak_rate)
                p_rate_min = p_peak_rate.min()
                p_rate_max = p_peak_rate.max()
                mean_p_rate = p_peak_rate.mean()

                #-----------------------------------
                # T_peak features
                #-----------------------------------
                t_peak_rate= (60/(np.diff(t_peaks)/fs)) # not a feature
                for i in range(ecgdata.shape[0]):
                    t_amp_leads[i] = (ecgdata[i][t_peaks]/voltage_res).mean()
                t_rate_std = t_peak_rate.std()
                t_rate_median = np.median(t_peak_rate)
                try:
                    t_rate_min = t_peak_rate.min()
                except:
                    print("Not able to calculate t_rate_min for sample {}".format(counter_all))
                    t_rate_min = 0
                try:  
                    t_rate_max = t_peak_rate.max()
                except:
                    t_rate_max = 0
                    print("Not able to calculate t_rate_max for sample {}".format(counter_all))
                mean_t_rate = t_peak_rate.mean()
                #-----------------------------------
                # T_offset features
                #-----------------------------------
                t_offset_rate= (60/(np.diff(t_offsets)/fs)) # not a feature
                t_offset_std = t_offset_rate.std()
                t_offset_median = np.median(t_offset_rate)
                try:
                    t_offset_min = t_offset_rate.min()
                except:
                    t_offset_min = 0
                    print("Not able to calculate t_offset_min for sample {}".format(counter_all))
                try:
                    t_offset_max = t_offset_rate.max()
                except:
                    t_offset_max = 0
                    print("Not able to calculate t_offset_max for sample {}".format(counter_all))
                mean_t_offset = t_offset_rate.mean()

                #-----------------------------------
                # T_onset features
                #-----------------------------------
                t_onsets_rate= (60/(np.diff(t_onsets)/fs)) # not a feature
                t_onsets_std = t_onsets_rate.std()
                t_onsets_median = np.median(t_onsets_rate)
                try:
                    t_onsets_min = t_onsets_rate.min()
                except:
                    t_onsets_min = 0
                    print("Not able to calculate t_onsets_min for sample {}".format(counter_all))
                try:
                    t_onsets_max = t_onsets_rate.max()
                except:
                    t_onsets_max = 0
                    print("Not able to calculate t_onsets_max for sample {}".format(counter_all))
                mean_t_onsets = t_onsets_rate.mean()

            except:
                print("Not able to get calculate discrete wavelet features")
                print("Future version will deal with this")
                labels_not_annotated.append(labels[counter_all])
                ecg_file_not_annotated.append(ecg_file)
                continue

            try:
                q_peaks, s_peaks = _other_peaks_detection(ecgdata,r_peaks,fs)

                #-----------------------------------
                # Q-peak features
                #-----------------------------------
                q_peak_rate= (60/(np.diff(q_peaks)/fs)) # not a feature
                for i in range(ecgdata.shape[0]):
                    q_amp_leads[i] = (ecgdata[i][q_peaks]/voltage_res).mean()
                q_rate_std = q_peak_rate.std()
                q_rate_median = np.median(q_peak_rate)
                q_rate_min = q_peak_rate.min()
                q_rate_max = q_peak_rate.max()
                mean_q_rate = q_peak_rate.mean()


                #-----------------------------------
                # S-peak features
                #-----------------------------------
                s_peak_rate= (60/(np.diff(s_peaks)/fs)) # not a feature
                for i in range(ecgdata.shape[0]):
                    s_amp_leads[i] = (ecgdata[i][s_peaks]/voltage_res).mean()
                s_rate_std = s_peak_rate.std()
                s_rate_median = np.median(s_peak_rate)
                s_rate_min = s_peak_rate.min()
                s_rate_max = s_peak_rate.max()
                mean_s_rate = s_peak_rate.mean()

            except:
                print("Not able to get calculate Q, S peaks and features related to them")
                print("Future version will deal with this")
                labels_not_annotated.append(labels[counter_all])
                ecg_file_not_annotated.append(ecg_file)
                continue

            labels_auto_annotated.append(labels[counter_auto_annotated])



            temp_array=np.asarray([gender,age,heartrate_std,heartrate_median,heartrate_min,heartrate_max,mean_heartrate_r, rmssd,r_amp_II_std,r_amp_II_min,r_amp_II_min, r_amp_leads[0],r_amp_leads[1],r_amp_leads[2],r_amp_leads[3],r_amp_leads[4],
                r_amp_leads[5],r_amp_leads[6], r_amp_leads[7],r_amp_leads[8], r_amp_leads[9], r_amp_leads[10], r_amp_leads[11],p_offset_std,p_offset_median,p_offset_min,p_offset_max,mean_p_offset,p_onsets_std, p_onsets_median,
                p_onsets_min,p_onsets_max,mean_p_onsets,ECG_baseline,p_rate_std,p_rate_median,p_rate_min,p_rate_max,mean_p_rate,p_amp_leads[0],p_amp_leads[1],p_amp_leads[2],p_amp_leads[3],p_amp_leads[4],p_amp_leads[5],
                p_amp_leads[6],p_amp_leads[7],p_amp_leads[8],p_amp_leads[9],p_amp_leads[10],p_amp_leads[11],q_rate_std,q_rate_median,q_rate_min,q_rate_max,mean_q_rate, q_amp_leads[0],q_amp_leads[1],q_amp_leads[2],q_amp_leads[3],
                q_amp_leads[4],q_amp_leads[5],q_amp_leads[6],q_amp_leads[7],q_amp_leads[8],q_amp_leads[9],q_amp_leads[10],q_amp_leads[11],s_rate_std, s_rate_median,s_rate_min,s_rate_max,mean_s_rate, s_amp_leads[0],s_amp_leads[1],
                s_amp_leads[2],s_amp_leads[3],s_amp_leads[4],s_amp_leads[5],s_amp_leads[6],s_amp_leads[7],s_amp_leads[8],s_amp_leads[9],s_amp_leads[10],s_amp_leads[11],t_rate_std,t_rate_median,t_rate_min,t_rate_max,mean_t_rate,
                t_amp_leads[0],t_amp_leads[1],t_amp_leads[2],t_amp_leads[3],t_amp_leads[4],t_amp_leads[5],t_amp_leads[6],t_amp_leads[7],t_amp_leads[8],t_amp_leads[9],t_amp_leads[10],t_amp_leads[11],t_offset_std,t_offset_median,
                t_offset_min,t_offset_max,mean_t_offset,t_onsets_std,t_onsets_median,t_onsets_min,t_onsets_max,mean_t_onsets
                ])
            

            feature_array[counter_auto_annotated] = temp_array

            counter_auto_annotated = counter_auto_annotated + 1

            print("{} out of {} succeeded".format(counter_auto_annotated,counter_all))


        FeatureNames = ['gender','age','R HR STD','R HR median','R HR min', 'R HR max','R HR mean','RMSSD','R amp II std','R amp II min','R amp II min_2', 'R amp leads I', 'R amp leads II', 'R amp lead III', 
                'R amp lead aVR','R amp lead aVL','R amp lead aVF', 'R amp V1','R amp V2','R amp V3','R amp V4','R amp V5','R amp V6','p_offset_std','p_offset_median','p_offset_min','p_offset_max',
                'mean_p_offset','p_onsets_std','p_onsets_median','p_onsets_min','p_onsets_max','mean_p_onsets','ECG_baseline','p_rate_std','p_rate_median','p_rate_min','p_rate_max','mean_p_rate', 
                'P amp leads I', 'P amp leads II', 'P amp lead III', 'P amp lead aVR','P amp lead aVL','P amp lead aVF', 'P amp V1','P amp V2','P amp V3','P amp V4','P amp V5','P amp V6','q_rate_std',
                'q_rate_median','q_rate_min','q_rate_max','mean_q_rate','Q amp leads I', 'Q amp leads II', 'Q amp lead III', 'Q amp lead aVR','Q amp lead aVL','Q amp lead aVF', 'Q amp V1','Q amp V2',
                'Q amp V3','Q amp V4','Q amp V5','Q amp V6','s_rate_std','s_rate_median','s_rate_min','s_rate_max','mean_s_rate','S amp leads I', 'S amp leads II', 'S amp lead III', 'S amp lead aVR',
                'S amp lead aVL','S amp lead aVF', 'S amp V1','S amp V2','S amp V3','S amp V4','S amp V5','S amp V6','t_rate_std','t_rate_median','t_rate_min','t_rate_max','mean_t_rate',
                'T amp leads I', 'T amp leads II', 'T amp lead III', 'T amp lead aVR','T amp lead aVL','T amp lead aVF', 'T amp V1','T amp V2','T amp V3','T amp V4','T amp V5','T amp V6','t_offset_std',
                't_offset_median','t_offset_min','t_offset_max','mean_t_offset','t_onsets_std','t_onsets_median','t_onsets_min','t_onsets_max','mean_t_onsets']
        feature_df = pd.DataFrame(feature_array)
        feature_df = feature_df.iloc[:counter_auto_annotated,:]
        feature_df.columns = FeatureNames
        feature_df['Labels'] = labels_auto_annotated

        self.features_out = feature_df
        self.files_for_manual_annotation = np.asarray(ecg_file_not_annotated)
        self.labels_for_manual_annotation = np.asarray(labels_not_annotated)
        print("files not annotated:",  self.files_for_manual_annotation)

        print("labels for files not annotated:",  self.labels_for_manual_annotation)

        return self.features_out, 

    def manual_annotation(self):
        pass_hash = input("Enter md5 hash: ")