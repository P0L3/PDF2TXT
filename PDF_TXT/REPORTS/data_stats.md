# Data statistics
- Using General dataset info from [try_pandaspickledataset.py](/try_pandaspickledataset.py)

## Full data - 26.3.2024.
``` shell
Number of rows:  171880
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 33197.49
Number of empty contents:               386  /  171880  =>  0.22 %
Number of <= 10000 length contents:  10920  /  171880  =>  6.35 %
<class 'pandas.core.frame.DataFrame'>
Index: 171880 entries, 0 to 10
Data columns (total 13 columns):
 #   Column                    Non-Null Count   Dtype 
---  ------                    --------------   ----- 
 0   Title                     171880 non-null  object
 1   Authors_and_Affiliations  171880 non-null  object
 2   Affiliations              171880 non-null  object
 3   DOI                       171880 non-null  object
 4   Authors                   171880 non-null  object
 5   Journal                   171880 non-null  object
 6   Date                      171880 non-null  object
 7   Subjects                  171880 non-null  object
 8   Abstract                  171880 non-null  object
 9   References                171880 non-null  object
 10  Content                   171880 non-null  object
 11  Keywords                  171880 non-null  object
 12  Style                     171880 non-null  object
dtypes: object(13)
memory usage: 18.4+ MB
None
                                               Title  ... Style
0  A   s y n o p t i c   c l i m a t o l o g y   ...  ...  html
1  S u m m e r   n i g h t - t i m e   t e m p e ...  ...  html
2  N e w   h o u r l y   e x t r e m e   p r e c ...  ...  html
3  T r e n d s   i n   d a i l y   p r e c i p i ...  ...  html
4  I m p a c t   o f   t h e   a i r   t e m p e ...  ...  html

```


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

``` shell
Number of rows:  6869 / 7103
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 35338.06
Number of empty contents:               68  /  6869  =>  0.9900000000000001 %
Number of <= 10000 length contents:  252  /  6869  =>  3.6700000000000004 %
<class 'pandas.core.frame.DataFrame'>
Index: 6869 entries, 0 to 13
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     6869 non-null   object
 1   Authors_and_Affiliations  6869 non-null   object
 2   Affiliations              6869 non-null   object
 3   DOI                       6869 non-null   object
 4   Authors                   6869 non-null   object
 5   Journal                   6869 non-null   object
 6   Date                      6869 non-null   object
 7   Subjects                  6869 non-null   object
 8   Abstract                  6869 non-null   object
 9   References                6869 non-null   object
 10  Content                   6869 non-null   object
 11  Keywords                  6869 non-null   object
 12  Style                     6869 non-null   int64 
dtypes: int64(1), object(12)
memory usage: 751.3+ KB
None
                                               Title  ... Style
0  [Simple additive effects are rare: a quantitat...  ...     2
1  [Neglecting acclimation of photosynthesis unde...  ...     5
2  [Does nitrogen deposition affect soil microfun...  ...     0
3  [An integrative synthesis to global amphibian ...  ...     5
4  [Biochar application as a tool to decrease soi...  ...     5
```

## CLIMD

``` shell
Number of rows:  3695 / 3943
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 43357.66
Number of empty contents:               25  /  3695  =>  0.6799999999999999 %
Number of <= 10000 length contents:  94  /  3695  =>  2.54 %
<class 'pandas.core.frame.DataFrame'>
Index: 3695 entries, 0 to 12
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     3695 non-null   object
 1   Authors_and_Affiliations  3695 non-null   object
 2   Affiliations              3695 non-null   object
 3   DOI                       3695 non-null   object
 4   Authors                   3695 non-null   object
 5   Journal                   3695 non-null   object
 6   Date                      3695 non-null   object
 7   Subjects                  3695 non-null   object
 8   Abstract                  3695 non-null   object
 9   References                3695 non-null   object
 10  Content                   3695 non-null   object
 11  Keywords                  3695 non-null   object
 12  Style                     3695 non-null   int64 
dtypes: int64(1), object(12)
memory usage: 404.1+ KB
None
                                               Title  ... Style
0  [The impact of inter-annual variability of ann...  ...     7
1  [Interdecadal change in the North Atlantic sto...  ...     1
2  [Decadal changes in the central tropical Pacif...  ...     7
3             [Predictability in a changing climate]  ...     7
4  [Reconciling roles of sulphate aerosol forcing...  ...     1

```


## PNAS
``` shell
Number of rows:  83099 / 88534
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 28258.25
Number of empty contents:               0  /  83099  =>  0.0 %
Number of <= 10000 length contents:  6303  /  83099  =>  7.580000000000001 %
<class 'pandas.core.frame.DataFrame'>
Index: 83099 entries, 0 to 14
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     83099 non-null  object
 1   Authors_and_Affiliations  83099 non-null  object
 2   Affiliations              83099 non-null  object
 3   DOI                       83099 non-null  object
 4   Authors                   83099 non-null  object
 5   Journal                   83099 non-null  object
 6   Date                      83099 non-null  object
 7   Subjects                  83099 non-null  object
 8   Abstract                  83099 non-null  object
 9   References                83099 non-null  object
 10  Content                   83099 non-null  object
 11  Keywords                  83099 non-null  object
 12  Style                     83099 non-null  object
dtypes: object(13)
memory usage: 8.9+ MB
None
                                               Title  ... Style
0  Root gravitropism is regulated by a transient ...  ...  html
1  Storage of cellular 5′ mRNA caps in P bodies f...  ...  html
2  General design principle for scalable neural c...  ...  html
3  Stimuli-responsive clustered nanoparticles for...  ...  html
4  Cullin neddylation inhibitor attenuates hyperg...  ...  html
```

## IJOC

``` shell
Number of rows:  3712 / 3825
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 22789.19
Number of empty contents:               0  /  3712  =>  0.0 %
Number of <= 10000 length contents:  1362  /  3712  =>  36.69 %
<class 'pandas.core.frame.DataFrame'>
Index: 3712 entries, 0 to 14
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     3712 non-null   object
 1   Authors_and_Affiliations  3712 non-null   object
 2   Affiliations              3712 non-null   object
 3   DOI                       3712 non-null   object
 4   Authors                   3712 non-null   object
 5   Journal                   3712 non-null   object
 6   Date                      3712 non-null   object
 7   Subjects                  3712 non-null   object
 8   Abstract                  3712 non-null   object
 9   References                3712 non-null   object
 10  Content                   3712 non-null   object
 11  Keywords                  3712 non-null   object
 12  Style                     3712 non-null   object
dtypes: object(13)
memory usage: 406.0+ KB
None
                                               Title  ... Style
0  A synoptic climatology of the near-surface win...  ...  html
1  Summer night-time temperature trends on the Ib...  ...  html
2  New hourly extreme precipitation regions and r...  ...  html
3  Trends in daily precipitation on the northeast...  ...  html
4  Impact of the air temperature and atmospheric ...  ...  html
```

## ENERPOL

``` shell
Number of rows:  866 / 1023
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 51407.07
Number of empty contents:               12  /  866  =>  1.39 %
Number of <= 10000 length contents:  31  /  866  =>  3.58 %
<class 'pandas.core.frame.DataFrame'>
Index: 866 entries, 0 to 10
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     866 non-null    object
 1   Authors_and_Affiliations  866 non-null    object
 2   Affiliations              866 non-null    object
 3   DOI                       866 non-null    object
 4   Authors                   866 non-null    object
 5   Journal                   866 non-null    object
 6   Date                      866 non-null    object
 7   Subjects                  866 non-null    object
 8   Abstract                  866 non-null    object
 9   References                866 non-null    object
 10  Content                   866 non-null    object
 11  Keywords                  866 non-null    object
 12  Style                     866 non-null    int64 
dtypes: int64(1), object(12)
memory usage: 94.7+ KB
None
                                               Title                           Authors_and_Affiliations  ...                                           Keywords Style
0  [Comparing electricity transitions: A historic...  [(Aleh Cherp, [a,b, ⁎ ,]), (Vadim Vinichenko, ...  ...  [Germany, Japan, Renewable electricity, Nuclea...     0
1  [Inequalities across cooling and heating in ho...  [(Luling Huang, [a , b , * ,]), (Destenie Nock...  ...  [Energy poverty , Residential energy consumpti...     1
2  [The search for the perfect match: Aligning po...  [(Gilbert Fridgen, [a , b ,]), (Anne Michaelis...  ...  [Energy transition , Flexibility market tradin...     1
3  [Opportunities for installed combined heat and...  [(Hyeunguk Ahn, [no_affiliation]), (William Mi...  ...  [Capacity factor , Ramping capability , Prime ...     1
4  [Reduced grid operating costs and renewable en...  [(Julia K. Szinai, [a , b , * ,]), (Colin J.R....  ...  [Plug-in electric vehicles , Mobility model , ...     1

```

## ECOAPP

``` shell
Number of rows:  4214 / 4469
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 36698.35
Number of empty contents:               0  /  4214  =>  0.0 %
Number of <= 10000 length contents:  553  /  4214  =>  13.120000000000001 %
<class 'pandas.core.frame.DataFrame'>
Index: 4214 entries, 0 to 11
Data columns (total 13 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Title                     4214 non-null   object
 1   Authors_and_Affiliations  4214 non-null   object
 2   Affiliations              4214 non-null   object
 3   DOI                       4214 non-null   object
 4   Authors                   4214 non-null   object
 5   Journal                   4214 non-null   object
 6   Date                      4214 non-null   object
 7   Subjects                  4214 non-null   object
 8   Abstract                  4214 non-null   object
 9   References                4214 non-null   object
 10  Content                   4214 non-null   object
 11  Keywords                  4214 non-null   object
 12  Style                     4214 non-null   object
dtypes: object(13)
memory usage: 460.9+ KB
None
                                               Title                           Authors_and_Affiliations  ...                                           Keywords Style
0  Linking marine ecosystems with the services th...  [(Fiona E. Culhane, 4, 3), (Christoper L. J. F...  ...  [biodiversity, conservation, ecological connec...  html
1  OVERSTORY-IMPOSED HETEROGENEITY IN SOLAR RADIA...  [(David D. Breshears, 2), (Paul M. Rich, 1), (...  ...  [Bouteloua gracilis, canopy and intercanopy ga...  html
2  Trait-mediated responses of caterpillar commun...  [(Benjamin M. L. Leroy, 11, 10, 9, 1), (Domini...  ...  [defoliation, DNA barcoding, Lepidoptera, Lyma...  html
3  HABITAT-SPECIFIC RECOVERY OF SHALLOW SUBTIDAL ...   [(Thomas A. Dean, 3, 1), (Stephen C. Jewett, 2)]  ...  [crabs, disturbance, eelgrass, epifauna, infau...  html
4  EVALUATING TRIBUTARY RESTORATION POTENTIAL FOR...          [(Phaedra Budy, 2), (Howard Schaller, 1)]  ...  [conservation, habitat, population viability, ...  html
```

## Full data - 5.3.2024.
``` shell
Number of rows:  180281
Columns:  Title, Authors_and_Affiliations, Affiliations, DOI, Authors, Journal, Date, Subjects, Abstract, References, Content, Keywords, Style
Average content length:                 33620.14
Number of empty contents:               664  /  180281  =>  0.37 %
Number of <= 10000 length contents:  10884  /  180281  =>  6.04 %
<class 'pandas.core.frame.DataFrame'>
Index: 180281 entries, 0 to 10
Data columns (total 13 columns):
 #   Column                    Non-Null Count   Dtype 
---  ------                    --------------   ----- 
 0   Title                     180281 non-null  object
 1   Authors_and_Affiliations  180281 non-null  object
 2   Affiliations              180281 non-null  object
 3   DOI                       180281 non-null  object
 4   Authors                   180281 non-null  object
 5   Journal                   180281 non-null  object
 6   Date                      180281 non-null  object
 7   Subjects                  180281 non-null  object
 8   Abstract                  180281 non-null  object
 9   References                180281 non-null  object
 10  Content                   180281 non-null  object
 11  Keywords                  180281 non-null  object
 12  Style                     180281 non-null  object
dtypes: object(13)
memory usage: 19.3+ MB
None
                                               Title                           Authors_and_Affiliations  ...                                           Keywords Style
0  A synoptic climatology of the near-surface win...  [(David A. Rahn, 2, 1, 3), (René D. Garreaud, ...  ...  [coastal wind, eastern boundary upwelling syst...  html
1  Summer night-time temperature trends on the Ib...  [(Arturo Sanchez-Lorenzo, 2, 4, 5), (Paulo Per...  ...  [atmospheric circulation patterns, canonical c...  html
2  New hourly extreme precipitation regions and r...  [(Motasem M. Darwish, 3, 9, 1, 4, 2, 8), (Mari...  ...  [extreme precipitation regions, hourly precipi...  html
3  Trends in daily precipitation on the northeast...  [(J. I. López-Moreno, 1, 3), (S. M. Vicente-Se...  ...  [daily precipitation, temporal trends, spatial...  html
4  Impact of the air temperature and atmospheric ...  [(Joanna Wibig, 2, 5, 3, 1, 4), (Piotr Piotrow...  ...  [atmospheric circulation, Clausius–Clapeyron, ...  html

[5 rows x 13 columns]
```
