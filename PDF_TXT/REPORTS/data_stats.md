# Data statistics
- Using General dataset info from [try_pandaspickledataset.py](/try_pandaspickledataset.py)

## JCLIMATE

``` shell
Number of rows:  13655 / 15325
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 41498.14
Number of empty contents:               95  /  13655  =>  0.7000000000000001 %
Number of <= {length} length contents:  298  /  13655  =>  2.18 %
<class 'pandas.core.frame.DataFrame'>
Index: 13655 entries, 0 to 12
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     13655 non-null  object
 1   Authors_and_Affiliations  13655 non-null  object
 2   Affiliations              13655 non-null  object
 3   DOI                       13655 non-null  object
 4   Authors                   13655 non-null  object
 5   Journal                   13655 non-null  object
 6   Date                      13655 non-null  object
 7   Subjects                  13655 non-null  object
 8   Abstract                  13655 non-null  object
 9   References                13655 non-null  object
 10  Content                   13655 non-null  object
 11  Keywords                  13655 non-null  object
 12  Style                     13655 non-null  int64 
dtypes: int64(1), object(12)
memory usage: 1.5+ MB
None
                                               Title Authors_and_Affiliations  ...     Keywords Style
0  [Projected Changes in Climate Extremes over th...      [no_auth_and_affil]  ...  no_keywords     1
1  [A Comparison of CCM2–BATS Skin Temperature an...      [no_auth_and_affil]  ...  no_keywords     0
2  [Cloud Radiative Feedbacks and El Nio–Southern...      [no_auth_and_affil]  ...  no_keywords     1
3  [Modulation of the Diurnal Cycle of Rainfall A...      [no_auth_and_affil]  ...  no_keywords     1
4    [A Vector Autoregressive ENSO Prediction Model]      [no_auth_and_affil]  ...  no_keywords     1


```

## JGRA

``` shell
Number of rows:  11976 / 14512
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 42485.31
Number of empty contents:               172  /  11976  =>  1.44 %
Number of <= {length} length contents:  1138  /  11976  =>  9.5 %
<class 'pandas.core.frame.DataFrame'>
Index: 11976 entries, 0 to 5
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     11976 non-null  object
 1   Authors_and_Affiliations  11976 non-null  object
 2   Affiliations              11976 non-null  object
 3   DOI                       11976 non-null  object
 4   Authors                   11976 non-null  object
 5   Journal                   11976 non-null  object
 6   Date                      11976 non-null  object
 7   Subjects                  11976 non-null  object
 8   Abstract                  11976 non-null  object
 9   References                11976 non-null  object
 10  Content                   11976 non-null  object
 11  Keywords                  11976 non-null  object
 12  Style                     11976 non-null  int64 
dtypes: int64(1), object(12)
memory usage: 1.3+ MB
None
                                               Title  ... Style
0  [Spatial Modeling of Local-Scale Biogenic and ...  ...     4
1  [Transition Zone Radiative Effects in Shortwav...  ...     7
2  [Developing PIDF Curves From Dynamically Downs...  ...     7
3  [Electric Field Variation in Clear and Convect...  ...     7
4                                         [no_title]  ...     0
```

## MDPI

``` shell
Number of rows:  52195 / 53755
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 37372.86
Number of empty contents:               292  /  52195  =>  0.5599999999999999 %
Number of <= {length} length contents:  853  /  52195  =>  1.63 %
<class 'pandas.core.frame.DataFrame'>
Index: 52195 entries, 0 to 830
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     52195 non-null  object
 1   Authors_and_Affiliations  52195 non-null  object
 2   Affiliations              52195 non-null  object
 3   DOI                       52195 non-null  object
 4   Authors                   52195 non-null  object
 5   Journal                   52195 non-null  object
 6   Date                      52195 non-null  object
 7   Subjects                  52195 non-null  object
 8   Abstract                  52195 non-null  object
 9   References                52195 non-null  object
 10  Content                   52195 non-null  object
 11  Keywords                  52195 non-null  object
 12  Style                     52195 non-null  object
dtypes: object(13)
memory usage: 5.6+ MB
None
                                               Title  ... Style
0  The Depth of Water Taken up by Walnut Trees du...  ...  html
1  Threat Degree Classification According to Habi...  ...  html
2  The Impacts of Vegetation Types and Soil Prope...  ...  html
3  Factors that Influence Climate Change Mitigati...  ...  html
4  A Holistic View of Soils in Delivering Ecosyst...  ...  html
```

## GCB

