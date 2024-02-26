from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import logging
import re
from nltk.corpus import words
import nltk
# nltk.download('words')
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
 
lemmatizer = WordNetLemmatizer()

ligatures_dict = [{'unicode': 'U+0132', 'sign': 'Ĳ', 'norm': 'IJ', 'Ĳ': 'IJ'}, {'unicode': 'U+0133', 'sign': 'ĳ', 'norm': 'ij', 'ĳ': 'ij'}, {'unicode': 'U+01C7', 'sign': 'Ǉ', 'norm': 'LJ', 'Ǉ': 'LJ'}, {'unicode': 'U+01C8', 'sign': 'ǈ', 'norm': 'Lj', 'ǈ': 'Lj'}, {'unicode': 'U+01C9', 'sign': 'ǉ', 'norm': 'lj', 'ǉ': 'lj'}, {'unicode': 'U+01CA', 'sign': 'Ǌ', 'norm': 'NJ', 'Ǌ': 'NJ'}, {'unicode': 'U+01CB', 'sign': 'ǋ', 'norm': 'Nj', 'ǋ': 'Nj'}, {'unicode': 'U+01CC', 'sign': 'ǌ', 'norm': 'nj', 'ǌ': 'nj'}, {'unicode': 'U+01F1', 'sign': 'Ǳ', 'norm': 'DZ', 'Ǳ': 'DZ'}, {'unicode': 'U+01F2', 'sign': 'ǲ', 'norm': 'Dz', 'ǲ': 'Dz'}, {'unicode': 'U+01F3', 'sign': 'ǳ', 'norm': 'dz', 'ǳ': 'dz'}, {'unicode': 'U+20A8', 'sign': '₨', 'norm': 'Rs', '₨': 'Rs'}, {'unicode': 'U+2116', 'sign': '№', 'norm': 'No', '№': 'No'}, {'unicode': 'U+2120', 'sign': '℠', 'norm': 'SM', '℠': 'SM'}, {'unicode': 'U+2121', 'sign': '℡', 'norm': 'TEL', '℡': 'TEL'}, {'unicode': 'U+2122', 'sign': '™', 'norm': 'TM', '™': 'TM'}, {'unicode': 'U+213B', 'sign': '℻', 'norm': 'FAX', '℻': 'FAX'}, {'unicode': 'U+2161', 'sign': 'Ⅱ', 'norm': 'II', 'Ⅱ': 'II'}, {'unicode': 'U+2162', 'sign': 'Ⅲ', 'norm': 'III', 'Ⅲ': 'III'}, {'unicode': 'U+2163', 'sign': 'Ⅳ', 'norm': 'IV', 'Ⅳ': 'IV'}, {'unicode': 'U+2165', 'sign': 'Ⅵ', 'norm': 'VI', 'Ⅵ': 'VI'}, {'unicode': 'U+2166', 'sign': 'Ⅶ', 'norm': 'VII', 'Ⅶ': 'VII'}, {'unicode': 'U+2167', 'sign': 'Ⅷ', 'norm': 'VIII', 'Ⅷ': 'VIII'}, {'unicode': 'U+2168', 'sign': 'Ⅸ', 'norm': 'IX', 'Ⅸ': 'IX'}, {'unicode': 'U+216A', 'sign': 'Ⅺ', 'norm': 'XI', 'Ⅺ': 'XI'}, {'unicode': 'U+216B', 'sign': 'Ⅻ', 'norm': 'XII', 'Ⅻ': 'XII'}, {'unicode': 'U+2171', 'sign': 'ⅱ', 'norm': 'ii', 'ⅱ': 'ii'}, {'unicode': 'U+2172', 'sign': 'ⅲ', 'norm': 'iii', 'ⅲ': 'iii'}, {'unicode': 'U+2173', 'sign': 'ⅳ', 'norm': 'iv', 'ⅳ': 'iv'}, {'unicode': 'U+2175', 'sign': 'ⅵ', 'norm': 'vi', 'ⅵ': 'vi'}, {'unicode': 'U+2176', 'sign': 'ⅶ', 'norm': 'vii', 'ⅶ': 'vii'}, {'unicode': 'U+2177', 'sign': 'ⅷ', 'norm': 'viii', 'ⅷ': 'viii'}, {'unicode': 'U+2178', 'sign': 'ⅸ', 'norm': 'ix', 'ⅸ': 'ix'}, {'unicode': 'U+217A', 'sign': 'ⅺ', 'norm': 'xi', 'ⅺ': 'xi'}, {'unicode': 'U+217B', 'sign': 'ⅻ', 'norm': 'xii', 'ⅻ': 'xii'}, {'unicode': 'U+3250', 'sign': '㉐', 'norm': 'PTE', '㉐': 'PTE'}, {'unicode': 'U+32CC', 'sign': '㋌', 'norm': 'Hg', '㋌': 'Hg'}, {'unicode': 'U+32CD', 'sign': '㋍', 'norm': 'erg', '㋍': 'erg'}, {'unicode': 'U+32CE', 'sign': '㋎', 'norm': 'eV', '㋎': 'eV'}, {'unicode': 'U+32CF', 'sign': '㋏', 'norm': 'LTD', '㋏': 'LTD'}, {'unicode': 'U+3371', 'sign': '㍱', 'norm': 'hPa', '㍱': 'hPa'}, {'unicode': 'U+3372', 'sign': '㍲', 'norm': 'da', '㍲': 'da'}, {'unicode': 'U+3373', 'sign': '㍳', 'norm': 'AU', '㍳': 'AU'}, {'unicode': 'U+3374', 'sign': '㍴', 'norm': 'bar', '㍴': 'bar'}, {'unicode': 'U+3375', 'sign': '㍵', 'norm': 'oV', '㍵': 'oV'}, {'unicode': 'U+3376', 'sign': '㍶', 'norm': 'pc', '㍶': 'pc'}, {'unicode': 'U+3377', 'sign': '㍷', 'norm': 'dm', '㍷': 'dm'}, {'unicode': 'U+337A', 'sign': '㍺', 'norm': 'IU', '㍺': 'IU'}, {'unicode': 'U+3380', 'sign': '㎀', 'norm': 'pA', '㎀': 'pA'}, {'unicode': 'U+3381', 'sign': '㎁', 'norm': 'nA', '㎁': 'nA'}, {'unicode': 'U+3383', 'sign': '㎃', 'norm': 'mA', '㎃': 'mA'}, {'unicode': 'U+3384', 'sign': '㎄', 'norm': 'kA', '㎄': 'kA'}, {'unicode': 'U+3385', 'sign': '㎅', 'norm': 'KB', '㎅': 'KB'}, {'unicode': 'U+3386', 'sign': '㎆', 'norm': 'MB', '㎆': 'MB'}, {'unicode': 'U+3387', 'sign': '㎇', 'norm': 'GB', '㎇': 'GB'}, {'unicode': 'U+3388', 'sign': '㎈', 'norm': 'cal', '㎈': 'cal'}, {'unicode': 'U+3389', 'sign': '㎉', 'norm': 'kcal', '㎉': 'kcal'}, {'unicode': 'U+338A', 'sign': '㎊', 'norm': 'pF', '㎊': 'pF'}, {'unicode': 'U+338B', 'sign': '㎋', 'norm': 'nF', '㎋': 'nF'}, {'unicode': 'U+338E', 'sign': '㎎', 'norm': 'mg', '㎎': 'mg'}, {'unicode': 'U+338F', 'sign': '㎏', 'norm': 'kg', '㎏': 'kg'}, {'unicode': 'U+3390', 'sign': '㎐', 'norm': 'Hz', '㎐': 'Hz'}, {'unicode': 'U+3391', 'sign': '㎑', 'norm': 'kHz', '㎑': 'kHz'}, {'unicode': 'U+3392', 'sign': '㎒', 'norm': 'MHz', '㎒': 'MHz'}, {'unicode': 'U+3393', 'sign': '㎓', 'norm': 'GHz', '㎓': 'GHz'}, {'unicode': 'U+3394', 'sign': '㎔', 'norm': 'THz', '㎔': 'THz'}, {'unicode': 'U+3396', 'sign': '㎖', 'norm': 'ml', '㎖': 'ml'}, {'unicode': 'U+3397', 'sign': '㎗', 'norm': 'dl', '㎗': 'dl'}, {'unicode': 'U+3398', 'sign': '㎘', 'norm': 'kl', '㎘': 'kl'}, {'unicode': 'U+3399', 'sign': '㎙', 'norm': 'fm', '㎙': 'fm'}, {'unicode': 'U+339A', 'sign': '㎚', 'norm': 'nm', '㎚': 'nm'}, {'unicode': 'U+339C', 'sign': '㎜', 'norm': 'mm', '㎜': 'mm'}, {'unicode': 'U+339D', 'sign': '㎝', 'norm': 'cm', '㎝': 'cm'}, {'unicode': 'U+339E', 'sign': '㎞', 'norm': 'km', '㎞': 'km'}, {'unicode': 'U+33A9', 'sign': '㎩', 'norm': 'Pa', '㎩': 'Pa'}, {'unicode': 'U+33AA', 'sign': '㎪', 'norm': 'kPa', '㎪': 'kPa'}, {'unicode': 'U+33AB', 'sign': '㎫', 'norm': 'MPa', '㎫': 'MPa'}, {'unicode': 'U+33AC', 'sign': '㎬', 'norm': 'GPa', '㎬': 'GPa'}, {'unicode': 'U+33AD', 'sign': '㎭', 'norm': 'rad', '㎭': 'rad'}, {'unicode': 'U+33B0', 'sign': '㎰', 'norm': 'ps', '㎰': 'ps'}, {'unicode': 'U+33B1', 'sign': '㎱', 'norm': 'ns', '㎱': 'ns'}, {'unicode': 'U+33B3', 'sign': '㎳', 'norm': 'ms', '㎳': 'ms'}, {'unicode': 'U+33B4', 'sign': '㎴', 'norm': 'pV', '㎴': 'pV'}, {'unicode': 'U+33B5', 'sign': '㎵', 'norm': 'nV', '㎵': 'nV'}, {'unicode': 'U+33B7', 'sign': '㎷', 'norm': 'mV', '㎷': 'mV'}, {'unicode': 'U+33B8', 'sign': '㎸', 'norm': 'kV', '㎸': 'kV'}, {'unicode': 'U+33B9', 'sign': '㎹', 'norm': 'MV', '㎹': 'MV'}, {'unicode': 'U+33BA', 'sign': '㎺', 'norm': 'pW', '㎺': 'pW'}, {'unicode': 'U+33BB', 'sign': '㎻', 'norm': 'nW', '㎻': 'nW'}, {'unicode': 'U+33BD', 'sign': '㎽', 'norm': 'mW', '㎽': 'mW'}, {'unicode': 'U+33BE', 'sign': '㎾', 'norm': 'kW', '㎾': 'kW'}, {'unicode': 'U+33BF', 'sign': '㎿', 'norm': 'MW', '㎿': 'MW'}, {'unicode': 'U+33C3', 'sign': '㏃', 'norm': 'Bq', '㏃': 'Bq'}, {'unicode': 'U+33C4', 'sign': '㏄', 'norm': 'cc', '㏄': 'cc'}, {'unicode': 'U+33C5', 'sign': '㏅', 'norm': 'cd', '㏅': 'cd'}, {'unicode': 'U+33C8', 'sign': '㏈', 'norm': 'dB', '㏈': 'dB'}, {'unicode': 'U+33C9', 'sign': '㏉', 'norm': 'Gy', '㏉': 'Gy'}, {'unicode': 'U+33CA', 'sign': '㏊', 'norm': 'ha', '㏊': 'ha'}, {'unicode': 'U+33CB', 'sign': '㏋', 'norm': 'HP', '㏋': 'HP'}, {'unicode': 'U+33CC', 'sign': '㏌', 'norm': 'in', '㏌': 'in'}, {'unicode': 'U+33CD', 'sign': '㏍', 'norm': 'KK', '㏍': 'KK'}, {'unicode': 'U+33CE', 'sign': '㏎', 'norm': 'KM', '㏎': 'KM'}, {'unicode': 'U+33CF', 'sign': '㏏', 'norm': 'kt', '㏏': 'kt'}, {'unicode': 'U+33D0', 'sign': '㏐', 'norm': 'lm', '㏐': 'lm'}, {'unicode': 'U+33D1', 'sign': '㏑', 'norm': 'ln', '㏑': 'ln'}, {'unicode': 'U+33D2', 'sign': '㏒', 'norm': 'log', '㏒': 'log'}, {'unicode': 'U+33D3', 'sign': '㏓', 'norm': 'lx', '㏓': 'lx'}, {'unicode': 'U+33D4', 'sign': '㏔', 'norm': 'mb', '㏔': 'mb'}, {'unicode': 'U+33D5', 'sign': '㏕', 'norm': 'mil', '㏕': 'mil'}, {'unicode': 'U+33D6', 'sign': '㏖', 'norm': 'mol', '㏖': 'mol'}, {'unicode': 'U+33D7', 'sign': '㏗', 'norm': 'PH', '㏗': 'PH'}, {'unicode': 'U+33D9', 'sign': '㏙', 'norm': 'PPM', '㏙': 'PPM'}, {'unicode': 'U+33DA', 'sign': '㏚', 'norm': 'PR', '㏚': 'PR'}, {'unicode': 'U+33DB', 'sign': '㏛', 'norm': 'sr', '㏛': 'sr'}, {'unicode': 'U+33DC', 'sign': '㏜', 'norm': 'Sv', '㏜': 'Sv'}, {'unicode': 'U+33DD', 'sign': '㏝', 'norm': 'Wb', '㏝': 'Wb'}, {'unicode': 'U+33FF', 'sign': '㏿', 'norm': 'gal', '㏿': 'gal'}, {'unicode': 'U+FB00', 'sign': 'ﬀ', 'norm': 'ff', 'ﬀ': 'ff'}, {'unicode': 'U+FB01', 'sign': 'ﬁ', 'norm': 'fi', 'ﬁ': 'fi'}, {'unicode': 'U+FB02', 'sign': 'ﬂ', 'norm': 'fl', 'ﬂ': 'fl'}, {'unicode': 'U+FB03', 'sign': 'ﬃ', 'norm': 'ffi', 'ﬃ': 'ffi'}, {'unicode': 'U+FB04', 'sign': 'ﬄ', 'norm': 'ffl', 'ﬄ': 'ffl'}, {'unicode': 'U+FB05', 'sign': 'ﬅ', 'norm': 'st', 'ﬅ': 'st'}, {'unicode': 'U+FB06', 'sign': 'ﬆ', 'norm': 'st', 'ﬆ': 'st'}, {'unicode': 'U+1F12D', 'sign': '🄭', 'norm': 'CD', '🄭': 'CD'}, {'unicode': 'U+1F12E', 'sign': '🄮', 'norm': 'WZ', '🄮': 'WZ'}, {'unicode': 'U+1F14A', 'sign': '🅊', 'norm': 'HV', '🅊': 'HV'}, {'unicode': 'U+1F14B', 'sign': '🅋', 'norm': 'MV', '🅋': 'MV'}, {'unicode': 'U+1F14C', 'sign': '🅌', 'norm': 'SD', '🅌': 'SD'}, {'unicode': 'U+1F14D', 'sign': '🅍', 'norm': 'SS', '🅍': 'SS'}, {'unicode': 'U+1F14E', 'sign': '🅎', 'norm': 'PPV', '🅎': 'PPV'}, {'unicode': 'U+1F14F', 'sign': '🅏', 'norm': 'WC', '🅏': 'WC'}, {'unicode': 'U+1F16A', 'sign': '🅪', 'norm': 'MC', '🅪': 'MC'}, {'unicode': 'U+1F16B', 'sign': '🅫', 'norm': 'MD', '🅫': 'MD'}, {'unicode': 'U+1F16C', 'sign': '🅬', 'norm': 'MR', '🅬': 'MR'}, {'unicode': 'U+1F190', 'sign': '🆐', 'norm': 'DJ', '🆐': 'DJ'}]
ligatures_conv = {'Ĳ': 'IJ', 'ĳ': 'ij', 'Ǉ': 'LJ', 'ǈ': 'Lj', 'ǉ': 'lj', 'Ǌ': 'NJ', 'ǋ': 'Nj', 'ǌ': 'nj', 'Ǳ': 'DZ', 'ǲ': 'Dz', 'ǳ': 'dz', '₨': 'Rs', '№': 'No', '℠': 'SM', '℡': 'TEL', '™': 'TM', '℻': 'FAX', 'Ⅱ': 'II', 'Ⅲ': 'III', 'Ⅳ': 'IV', 'Ⅵ': 'VI', 'Ⅶ': 'VII', 'Ⅷ': 'VIII', 'Ⅸ': 'IX', 'Ⅺ': 'XI', 'Ⅻ': 'XII', 'ⅱ': 'ii', 'ⅲ': 'iii', 'ⅳ': 'iv', 'ⅵ': 'vi', 'ⅶ': 'vii', 'ⅷ': 'viii', 'ⅸ': 'ix', 'ⅺ': 'xi', 'ⅻ': 'xii', '㉐': 'PTE', '㋌': 'Hg', '㋍': 'erg', '㋎': 'eV', '㋏': 'LTD', '㍱': 'hPa', '㍲': 'da', '㍳': 'AU', '㍴': 'bar', '㍵': 'oV', '㍶': 'pc', '㍷': 'dm', '㍺': 'IU', '㎀': 'pA', '㎁': 'nA', '㎃': 'mA', '㎄': 'kA', '㎅': 'KB', '㎆': 'MB', '㎇': 'GB', '㎈': 'cal', '㎉': 'kcal', '㎊': 'pF', '㎋': 'nF', '㎎': 'mg', '㎏': 'kg', '㎐': 'Hz', '㎑': 'kHz', '㎒': 'MHz', '㎓': 'GHz', '㎔': 'THz', '㎖': 'ml', '㎗': 'dl', '㎘': 'kl', '㎙': 'fm', '㎚': 'nm', '㎜': 'mm', '㎝': 'cm', '㎞': 'km', '㎩': 'Pa', '㎪': 'kPa', '㎫': 'MPa', '㎬': 'GPa', '㎭': 'rad', '㎰': 'ps', '㎱': 'ns', '㎳': 'ms', '㎴': 'pV', '㎵': 'nV', '㎷': 'mV', '㎸': 'kV', '㎹': 'MV', '㎺': 'pW', '㎻': 'nW', '㎽': 'mW', '㎾': 'kW', '㎿': 'MW', '㏃': 'Bq', '㏄': 'cc', '㏅': 'cd', '㏈': 'dB', '㏉': 'Gy', '㏊': 'ha', '㏋': 'HP', '㏌': 'in', '㏍': 'KK', '㏎': 'KM', '㏏': 'kt', '㏐': 'lm', '㏑': 'ln', '㏒': 'log', '㏓': 'lx', '㏔': 'mb', '㏕': 'mil', '㏖': 'mol', '㏗': 'PH', '㏙': 'PPM', '㏚': 'PR', '㏛': 'sr', '㏜': 'Sv', '㏝': 'Wb', '㏿': 'gal', 'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl', 'ﬅ': 'st', 'ﬆ': 'st', '🄭': 'CD', '🄮': 'WZ', '🅊': 'HV', '🅋': 'MV', '🅌': 'SD', '🅍': 'SS', '🅎': 'PPV', '🅏': 'WC', '🅪': 'MC', '🅫': 'MD', '🅬': 'MR', '🆐': 'DJ'}
ligatures_list = ['Ĳ', 'ĳ', 'Ǉ', 'ǈ', 'ǉ', 'Ǌ', 'ǋ', 'ǌ', 'Ǳ', 'ǲ', 'ǳ', '₨', '№', '℠', '℡', '™', '℻', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅺ', 'Ⅻ', 'ⅱ', 'ⅲ', 'ⅳ', 'ⅵ', 'ⅶ', 'ⅷ', 'ⅸ', 'ⅺ', 'ⅻ', '㉐', '㋌', '㋍', '㋎', '㋏', '㍱', '㍲', '㍳', '㍴', '㍵', '㍶', '㍷', '㍺', '㎀', '㎁', '㎃', '㎄', '㎅', '㎆', '㎇', '㎈', '㎉', '㎊', '㎋', '㎎', '㎏', '㎐', '㎑', '㎒', '㎓', '㎔', '㎖', '㎗', '㎘', '㎙', '㎚', '㎜', '㎝', '㎞', '㎩', '㎪', '㎫', '㎬', '㎭', '㎰', '㎱', '㎳', '㎴', '㎵', '㎷', '㎸', '㎹', '㎺', '㎻', '㎽', '㎾', '㎿', '㏃', '㏄', '㏅', '㏈', '㏉', '㏊', '㏋', '㏌', '㏍', '㏎', '㏏', '㏐', '㏑', '㏒', '㏓', '㏔', '㏕', '㏖', '㏗', '㏙', '㏚', '㏛', '㏜', '㏝', '㏿', 'ﬀ', 'ﬁ', 'ﬂ', 'ﬃ', 'ﬄ', 'ﬅ', 'ﬆ', '🄭', '🄮', '🅊', '🅋', '🅌', '🅍', '🅎', '🅏', '🅪', '🅫', '🅬', '🆐']
pattern = "Ĳ|ĳ|Ǉ|ǈ|ǉ|Ǌ|ǋ|ǌ|Ǳ|ǲ|ǳ|₨|№|℠|℡|™|℻|Ⅱ|Ⅲ|Ⅳ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅺ|Ⅻ|ⅱ|ⅲ|ⅳ|ⅵ|ⅶ|ⅷ|ⅸ|ⅺ|ⅻ|㉐|㋌|㋍|㋎|㋏|㍱|㍲|㍳|㍴|㍵|㍶|㍷|㍺|㎀|㎁|㎃|㎄|㎅|㎆|㎇|㎈|㎉|㎊|㎋|㎎|㎏|㎐|㎑|㎒|㎓|㎔|㎖|㎗|㎘|㎙|㎚|㎜|㎝|㎞|㎩|㎪|㎫|㎬|㎭|㎰|㎱|㎳|㎴|㎵|㎷|㎸|㎹|㎺|㎻|㎽|㎾|㎿|㏃|㏄|㏅|㏈|㏉|㏊|㏋|㏌|㏍|㏎|㏏|㏐|㏑|㏒|㏓|㏔|㏕|㏖|㏗|㏙|㏚|㏛|㏜|㏝|㏿|ﬀ|ﬁ|ﬂ|ﬃ|ﬄ|ﬅ|ﬆ|🄭|🄮|🅊|🅋|🅌|🅍|🅎|🅏|🅪|🅫|🅬|🆐"



def pdf2html(target="./SAMPLE/NCLIMATE/s41558-020-00938-y_Heat_Tolerance_In_Ectotherms_Scales_Predictably_With_Body_Size_.pdf", line_margin=0.5, all_texts=True):
    """
    Converts a PDF file to HTML format.

    Args:
        target (str): Path to the PDF file to be converted. Default is "./SAMPLE/NCLIMATE/s41558-020-00938-y_Heat_Tolerance_In_Ectotherms_Scales_Predictably_With_Body_Size_.pdf".
        line_margin (float): Margin between lines in the output HTML. Default is 0.5.
        all_texts (bool): If True, extracts all text from the PDF. If False, only extracts text from visible elements. Default is True.

    Returns:
        str: HTML representation of the PDF content.

    Raises:
        None.

    Note:
        This function utilizes the `extract_text_to_fp` method from PyPDF2 library to extract text from the PDF.
        If the PDF cannot be read, a warning message is logged, and None is returned.

    """

    try:
        output_string = StringIO()

        with open(target, 'rb') as fin:
            extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)

        return output_string.getvalue()
    except:
        warning_message = f"Unable to read PDF. Skipping..."
        logging.warning(warning_message)
        return None
    
def check_if_ium(soup):
    """
    Check if the provided BeautifulSoup 'soup' object indicates incomplete Unicode mappings (ium).

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

    Returns:
    - bool: True if incomplete Unicode mappings are found, False otherwise.

    The function searches for a 'div' element in the provided 'soup' object and iterates through its
    next siblings until a text length of at least 50 characters is found or no more siblings are present.
    It then uses a regular expression to check if the text contains at least three consecutive instances
    of the pattern "(cid:\d+)" which might indicate incomplete Unicode mappings.
    """
    elem = soup.find("div")
    while len(elem.text) < 50 and not type(elem) == type(None):
        elem = elem.find_next()

    if type(elem) == type(None):
        raise Exception("NO div element found!")
    
    return bool(re.search("(\(cid:\d+\)){3,}", elem.text))

def add_custom_tag_after_element(soup, target_element, tag_name, tag_content, style_attributes):
    """
    Add a custom tag with specified content after a specific element in the BeautifulSoup 'soup' object.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
    - target_element (Tag): The target element after which the new tag will be added.
    - tag_name (str): The name of the custom tag to be added.
    - tag_content (str): The content to be placed inside the custom tag.

    Returns:
    - BeautifulSoup: The modified BeautifulSoup object.
    """
    if type(target_element) == type(None):
        warning_message = "Tag is not added correctly -> Implies that the target element wasn't found correctly prior"
        logging.warning(warning_message)
        return soup
    new_tag = soup.new_tag(tag_name)
    new_tag.string = tag_content
    new_tag.attrs.update(style_attributes)
    target_element.insert_after(new_tag)
    return soup

def find_custom_element_by_regex(soup, regex="^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n+", reverese=True):
    """
    Finds a custom HTML element within a BeautifulSoup object based on a given regular expression.

    Args:
    - soup: BeautifulSoup object representing HTML content.
    - regex (str): Regular expression pattern to search for within the text content of HTML elements.
    - reverse (bool): If True, searches for the element in reverse order (from the last element to the first).

    Returns:
    - elem: The BeautifulSoup element that matches the specified regex pattern, or None if not found.
    """
    if reverese:
        elem = soup.find_all('div')[-1]
        while type(elem) != type(None):
            if re.search(regex, elem.text):   
                # print(elem.text)
                break
            elem = elem.find_previous()
    else:
        elem = soup.find('div')
        while type(elem) != type(None):
            if re.search(regex, elem.text):   
                # print(elem.text)
                break
            elem = elem.find_next()

    return elem

def likely_word(tokenbefore, token, tokenafter):
    """
    Check if the combination of tokens (current, before, and after) constitutes a likely word.

    Args:
        tokenbefore (str): The token preceding the current token.
        token (str): The current token.
        tokenafter (str): The token following the current token.

    Returns:
        tuple: A tuple containing the following elements:
            - str: The modified tokenbefore string, after cleaning and processing.
            - str: The modified token string, after cleaning and processing.
            - str: The modified tokenafter string, after cleaning and processing.
            - int: Flag indicating if a likely word is found (1) or not (0).
    """

    temp_token = token
    temp_tokenbefore = tokenbefore
    temp_tokenafter = tokenafter

    # Clean from punctuation and simmilar
    token = re.sub(r"[(),.!?;]+", "", token).lower()
    tokenbefore = re.sub(r"[(),.!?;]+", "", tokenbefore).lower()
    tokenafter = re.sub(r"[(),.!?;]+", "", tokenafter).lower()

    # Deal with concatenated words, such as "age-specific"
    tokenbefore = re.sub(r"\w+-", "", tokenbefore)

    replace_token = ""
    
    if tokenbefore+token+tokenafter in words.words() or lemmatizer.lemmatize(tokenbefore+token+tokenafter) in words.words() or lemmatizer.lemmatize(tokenbefore+token+tokenafter, pos='v') in words.words():
        return replace_token, temp_tokenbefore+temp_token+temp_tokenafter, replace_token, 1
    
    elif token+tokenafter in words.words() or lemmatizer.lemmatize(token+tokenafter) in words.words() or lemmatizer.lemmatize(token+tokenafter, pos='v') in words.words():
        return temp_tokenbefore, temp_token+temp_tokenafter, replace_token, 1
    
    elif tokenbefore+token in words.words() or lemmatizer.lemmatize(tokenbefore+token) in words.words() or lemmatizer.lemmatize(tokenbefore+token, pos='v') in words.words():
        return replace_token, temp_tokenbefore+temp_token, temp_tokenafter, 1
    
    elif token in words.words() in words.words():
        return temp_tokenbefore, temp_token, temp_tokenafter, 1
    
    else:
        if len(temp_token) > 2:
            return temp_tokenbefore, temp_token, temp_tokenafter, 1
        else: 
            # print(temp_tokenbefore, temp_token, temp_tokenafter)
            return temp_tokenbefore, replace_token, temp_tokenafter, 0
        
def fi_cleaner(text):
    """
    Cleans the text by replacing ligatures with their corresponding characters.
    
    Args:
    text (str): The input text to be cleaned.
    
    Returns:
    str: The cleaned text with ligatures replaced.
    """
    
    tokens = text.split()
    
    for i, word in enumerate(tokens):
        count = 0

        for j, c in enumerate(word):
            if c in ligatures_list:
                if (j == 0 or j == len(word)-1):
                    # temp = tokens[i]
                    # print(20*"-")
                    # print(i, "\t", tokens[i-1], tokens[i], tokens[i+1], end="----")
                    count += 1
                    try:
                        tokens[i-1], tokens[i], tokens[i+1], f = likely_word(tokens[i-1], re.sub(pattern, lambda m: ligatures_conv.get(m.group(0)), tokens[i]), tokens[i+1])
                    except:
                        continue
                    # if f == 0:
                    #     fi_counter_unsolved.append((temp, tokens[i]))
                    # else:
                    #     fi_counter_solved.append((temp, tokens[i]))
                else:
                    tokens[i] = re.sub(pattern, lambda m: ligatures_conv.get(m.group(0)), tokens[i])
                    count += 1
                # print(tokens[i-1], tokens[i], tokens[i+1])
        if count > 1: # Check if some word containes multiple ligatures
            print(i, "\t", tokens[i-1], tokens[i], tokens[i+1])
            warning_message = f"Multiple ligatures in single word!"
            logging.warning(warning_message)
            
    return " ".join(tokens)
    
