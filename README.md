 # VOID PREDICTION - NUCLEATE VOID PREDICTION USING MACHINE LEARNING TECHNIQUES

This research want to answers this question, what commonalities do these microstructural features of grain boundaries share that make them the preferred sites for void nucleation?

Dependencies
============
python3
requirements.txt

Usage
=====

Use the following files 

- GB_printer.py:   Show a specific or all the avaible samples as 5 figures and there are saved on the output/[sample_name].
  		- [sample_name]_[number_detected_voids].png -> Finally selected gb (green).
		- [sample_name]_categories.png 		    -> Old selected gb (green), new selected gb (pink), refused gb (orange).
		- [sample_name]_drawing.png 		    -> Detected Voids on the original EBSD.
		- [sample_name]_drawing.png		    -> Isolate voids, size and shape.
		- [sample_name]_parameter.png		    -> Selected gb and the corresponding proximity parameter [prox_par = (original_len + reconstructed_len)/(void_radi) ].

- selected_txt_generator.py: Generate a output/[sample_name]/selected.txt file for each sample where contains the following information for the selected gb
  	        - Column 1:    Selected grain boundary location of the input sample
		- Column 2:    Void parameter value
		- Column 3:    Distance from the grain boundary to the center void
		- Column 4:    Void ID
		- Column 5:    Sorted GB by distance from the center of the void
		- Column 6-7:  Supposed intersections point of GB with void edge, x and y
		- Column 8-9:  Supposed GB junction point
		- Column 10:   Reconstructed length of GB continuity
		- Column 11:   Proximity parameter.

- modules/df_saver: Generate the corresponding two dataframe for each sample:
  		- /output/[sample_name]/df_all.csv 	 -> All the grain boundaries of the sample with each featurs values.
		- /output/[sample_name]/df_selected.csv  -> Only affected gb by the nucleation void of the previous dataframe.

		And it generate a global dataframe appending all the samples in the same way:
  		- /output/total_gb_df.csv      -> All the grain boundaries from all the samples.
		- /output/total_sel_df.csv     -> Only all affected gb by the nucleation void from all the samples.

- /modules/sigma_value.py: Generate the .in file (no save) and apply it on wield code to generate the energy_output file, where it saves all the computed sigma values for each gb at the sample.
 
- BCC_Ploting.py & HCP_Ploting.py: Generate the structure figure applied on the wield code.

- vp_tester.py: Generate a picture of the reconstruction gb and junction detection.

- '/ml' directory: All the stadistical and machine learning applications on the dataset.
  ind_dataset.ipynb , clas_model.ipynb , LDA_Comm.ipynb , reg_model.ipynb , Test_dataset.ipynb , testing_analysis.ipynb

- Mis_Trace_Angle.ipynb -> Misorientation and trace angle plots and verifications.
- wield_gb_input.ipynb  -> wield code plots.
