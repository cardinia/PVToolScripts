import os
import sys
import calendar
import optparse
import importlib
import sqlalchemy
import subprocess
import CondCore.Utilities.conddblib as conddb

##############################################
def execme(command, dryrun=False):
##############################################
    '''Wrapper for executing commands.
    '''
    if dryrun:
        print command
    else:
        print " * Executing: %s ..." % (command)
        os.system(command)
        print " * Executed!"

##############################################
def print_times(inputRun):
##############################################
    con = conddb.connect(url = conddb.make_url())
    session = con.session()
    RunInfo = session.get_dbtype(conddb.RunInfo)
    
    bestRun = session.query(RunInfo.run_number,RunInfo.start_time, RunInfo.end_time).filter(RunInfo.run_number == inputRun).first()
    if bestRun is None:
        raise Exception("Run %s can't be matched with an existing run in the database." %options.runNumber)
    
    start= bestRun[1]
    stop = bestRun[2]
    
    bestRunStartTime = calendar.timegm( bestRun[1].utctimetuple() ) << 32
    bestRunStopTime  = calendar.timegm( bestRun[2].utctimetuple() ) << 32
    
    return (start,stop)
    #print "run start time:",start,"(",bestRunStartTime,")"
    #print "run stop time: ",stop,"(",bestRunStopTime,")"


##############################################
def main():
##############################################
    
    listOfRuns = [294927,294928,294929,294931,294932,294933,294934,294935,294936,294937,294939,294940,294947,294949,294950,294951,294952,294953,294954,294955,294956,294957,294960,294986,294987,294988,294990,294992,294993,294995,294997,294999,295001,295122,295123,295124,295125,295126,295127,295128,295129,295130,295131,295132,295133,295134,295135,295192,295193,295194,295197,295198,295199,295200,295201,295202,295203,295204,295208,295209,295210,295315,295318,295319,295320,295321,295322,295323,295324,295325,295326,295327,295328,295329,295330,295331,295332,295334,295335,295336,295337,295339,295340,295341,295342,295343,295344,295345,295346,295347,295348,295349,295371,295376,295377,295378,295379,295380,295381,295390,295391,295392,295393,295394,295395,295436,295437,295438,295439,295440,295441,295442,295443,295444,295445,295446,295447,295448,295449,295450,295451,295452,295453,295454,295455,295456,295457,295458,295459,295460,295463,295600,295602,295603,295604,295605,295606,295607,295608,295610,295613,295628,295632,295634,295635,295636,295637,295638,295639,295640,295641,295642,295644,295645,295646,295647,295648,295649,295650,295651,295652,295655,295953,295969,295976,295977,296070,296071,296073,296074,296076,296077,296078,296079,296081,296082,296083,296084,296085,296086,296087,296088,296089,296090,296091,296092,296093,296094,296095,296096,296097,296098,296099,296100,296101,296102,296103,296104,296107,296108,296109,296110,296111,296112,296113,296114,296115,296116,296168,296172,296173,296174,296641,296642,296643,296644,296646,296647,296663,296664,296665,296666,296668,296669,296671,296674,296675,296676,296677,296678,296679,296702,296786,296787,296788,296789,296790,296791,296795,296796,296797,296799,296800,296801,296802,296866,296867,296868,296869,296870,296871,296872,296873,296874,296875,296876,296877,296878,296879,296880,296881,296887,296888,296895,296897,296898,296899,296900,296901,296902,296966,296967,296968,296969,296970,296971,296972,296976,296977,296978,296979,296980,297003,297004,297006,297007,297009,297010,297011,297012,297015,297016,297017,297018,297019,297047,297048,297049,297050,297056,297057,297099,297100,297101,297113,297114,297168,297169,297170,297171,297175,297176,297177,297178,297179,297180,297181,297211,297215,297218,297219,297224,297225,297227,297281,297282,297283,297284,297285,297286,297287,297288,297289,297290,297291,297292,297293,297296,297308,297359,297411,297424,297425,297426,297429,297430,297431,297432,297433,297434,297435,297467,297468,297469,297474,297483,297484,297485,297486,297487,297488,297494,297495,297496,297497,297498,297499,297501,297502,297503,297504,297505,297557,297558,297562,297563,297598,297599,297603,297604,297605,297606,297620,297656,297657,297658,297659,297660,297661,297662,297663,297664,297665,297666,297670,297671,297672,297673,297674,297675,297678,297722,297723,298653,298678,298996,298997,298998,299000,299042,299061,299062,299064,299065,299067,299096,299149,299178,299180,299183,299184,299185,299996,300018,300027,300043,300079,300087,300088,300105,300106,300107,300117,300122,300123,300124,300155,300156,300157,300226,300233,300234,300235,300236,300237,300238,300239,300240,300280,300281,300282,300283,300284,300364,300365,300366,300367,300368,300369,300370,300371,300372,300373,300374,300375,300389,300390,300391,300392,300393,300394,300395,300396,300397,300398,300399,300400,300401,300459,300461,300462,300463,300464,300466,300467,300497,300498,300499,300500,300514,300515,300516,300517,300538,300539,300545,300548,300551,300552,300558,300560,300574,300575,300576,300631,300632,300633,300635,300636,300673,300674,300675,300676,300742,300777,300780,300785,300806,300811,300812,300816,300817,301046,301086,301141,301142,301161,301165,301179,301180,301183,301281,301283,301298,301323,301330,301359,301383,301384,301391,301392,301393,301394,301395,301396,301397,301398,301399,301417,301447,301448,301449,301450,301461,301472,301473,301474,301475,301476,301480,301519,301524,301525,301528,301529,301530,301531,301532,301567,301627,301664,301665,301694,301912,301913,301914,301941,301959,301960,302131,302159,302163,302165,302166,302225,302228,302229,302239,302240,302262,302263,302277,302279,302280,302322,302328,302337,302342,302343,302344,302349,302350,302388,302392,302393,302448,302472,302473,302474,302475,302476,302479,302484,302485,302486,302487,302488,302489,302490,302491,302492,302493,302494,302509,302513,302522,302523,302525,302526,302548,302550,302551,302553,302554,302555,302563,302564,302565,302566,302567,302569,302570,302571,302572,302573,302596,302597,302634,302635,302646,302651,302654,302660,302661,302663,303818,303819,303824,303825,303832,303838,303885,303948,303989,303998,303999,304000,304062,304119,304120,304125,304144,304158,304169,304170,304196,304197,304198,304199,304200,304204,304209,304291,304292,304333,304354,304366,304446,304447,304448,304449,304451,304452,304505,304506,304507,304508,304562,304616,304625,304626,304654,304655,304661,304662,304663,304671,304672,304737,304738,304739,304740,304776,304777,304778,304797,305040,305043,305044,305045,305046,305059,305062,305063,305064,305081,305112,305113,305114,305178,305179,305180,305181,305182,305183,305184,305185,305186,305188,305202,305204,305207,305208,305234,305236,305237,305247,305248,305249,305250,305252,305282,305310,305311,305312,305313,305314,305336,305338,305341,305349,305350,305351,305358,305364,305365,305366,305376,305377,305405,305406,305440,305441,305516,305517,305518,305586,305588,305589,305590,305636,305766,305809,305814,305821,305832,305840,305841,305842,305862,305898,305902,305967,306029,306030,306036,306037,306038,306041,306042,306048,306049,306051,306091,306092,306093,306095,306121,306122,306125,306126,306134,306135,306137,306138,306139,306153,306154,306155,306169,306170,306171,306416,306417,306418,306419,306420,306422,306423,306425,306432,306454,306455,306456,306457,306458,306459,306460,306461,306462,306546,306548,306549,306550,306553,306563,306572,306580,306584,306595,306598,306604,306629,306630,306631,306636,306645,306646,306647,306651,306652,306653,306654,306656,306657,306896,306897,306926,306929,306936,307014,307015,307016,307017,307042,307044,307045,307046,307047,307048,307049,307050,307051,307052,307053,307054,307055,307062,307063,307073,307075,307076,307082]

#[297047,297048,297049,297050,297056,297057,297099,297100,297101,297113,297114,297168,297169,297170,297171,297175,297176,297177,297178,297179,297180,297181,297211,297215,297218,297219,297224,297225,297227,297281,297282,297283,297284,297285,297286,297287,297288,297289,297290,297291,297292,297293,297296,297308,297359,297411,297424,297425,297426,297429,297430,297431,297432,297433,297434,297435,297467,297468,297469,297474,297483,297484,297485,297486,297487,297488,297494,297495,297496,297497,297498,297499,297501,297502,297503,297504,297505,297557,297558,297562,297563,297598,297599,297603,297604,297605,297606,297620,297656,297657,297658,297659,297660,297661,297662,297663,297664,297665,297666,297670,297671,297672,297673,297674,297675,297678,297722,297723,298653,298678,298996,298997,298998,299000,299042,299061,299062,299064,299065,299067,299096,299149,299178,299180,299183,299184,299185,299996,300018,300027,300043,300079,300087,300088,300105,300106,300107,300117,300122,300123,300124,300155,300156,300157,300226,300233,300234,300235,300236,300237,300238,300239,300240,300280,300281,300282,300283,300284,300364,300365,300366,300367,300368,300369,300370,300371,300372,300373,300374,300375,300389,300390,300391,300392,300393,300394,300395,300396,300397,300398,300399,300400,300401,300459,300461,300462,300463,300464,300466,300467,300497,300498,300499,300500,300514,300515,300516,300517,300538,300539,300545,300548,300551,300552,300558,300560,300574,300575,300576,300631,300632,300633,300635,300636,300673,300674,300675,300676,300742,300777,300780,300785,300806,300811,300812,300816,300817,301046,301086,301141,301142,301161,301165,301179,301180,301183,301281,301283,301298,301323,301330,301359,301383,301384,301391,301392,301393,301394,301395,301396,301397,301398,301399,301417,301447,301448,301449,301450,301461,301472,301473,301474,301475,301476,301480,301519,301524,301525,301528,301529,301530,301531,301532,301567,301627,301664,301665,301694,301912,301913,301914,301941,301959,301960,302131,302159,302163,302165,302166,302225,302228,302229,302239,302240,302262,302263,302277,302279,302280,302322,302328,302337,302342,302343,302344,302349,302350,302388,302392,302393,302448,302472,302473,302474,302475,302476,302479,302484,302485,302486,302487,302488,302489,302490,302491,302492,302493,302494,302509,302513,302522,302523,302525,302526,302548,302550,302551,302553,302554,302555,302563,302564,302565,302566,302567,302569,302570,302571,302572,302573,302596,302597,302634,302635,302646,302651,302654,302660,302661,302663,303818,303819,303824,303825,303832,303838,303885,303948,303989,303998,303999,304000,304062,304119,304120,304125,304144,304158,304169,304170,304196,304197,304198,304199,304200,304204,304209,304291,304292,304333,304354,304366,304446,304447,304448,304449,304451,304452,304505,304506,304507,304508,304562,304616,304625,304626,304654,304655,304661,304662,304663,304671,304672,304737,304738,304739,304740,304776,304777,304778,304797,305040,305043,305044,305045,305046,305059,305062,305063,305064,305081,305112,305113,305114,305178,305179,305180,305181,305182,305183,305184,305185,305186,305188,305202,305204,305207,305208,305234,305236,305237,305247,305248,305249,305250,305252,305282,305310,305311,305312,305313,305314,305336,305338,305341,305349,305350,305351,305358,305364,305365,305366,305376,305377,305405,305406,305440,305441,305516,305517,305518,305586,305588,305589,305590,305636,305766,305809,305814,305821,305832,305840,305841,305842,305862,305898,305902,305967,306029,306030,306036,306037,306038,306041,306042,306048,306049,306051,306091,306092,306093,306095,306121,306122,306125,306126,306134,306135,306137,306138,306139,306153,306154,306155,306169,306170,306171,306416,306417,306418,306419,306420,306422,306423,306425,306432,306454,306455,306456,306457,306458,306459,306460,306461,306462,306546,306548,306549,306550,306553,306563,306572,306580,306584,306595,306598,306604,306629,306630,306631,306636,306645,306646,306647,306651,306652,306653,306654,306656,306657,306896,306897,306926,306929,306936,307014,307015,307016,307017,307042,307044,307045,307046,307047,307048,307049,307050,307051,307052,307053,307054,307055,307062,307063,307073,307075,307076,307082]

#[297047,297048,297049,297050,297056,297057,297099,297100,297101,297113,297114,297168,297169,297170,297171,297175,297176,297177,297178,297179,297180,297181,297211,297215,297218,297219,297224,297225,297227,297281,297282,297283,297284,297285,297286,297287,297288,297289,297290,297291,297292,297293,297296,297308,297359,297411,297424,297425,297426,297429,297430,297431,297432,297433,297434,297435,297467,297468,297469,297474,297483,297484,297485,297486,297487,297488,297494,297495,297496,297497,297498,297499,297501,297502,297503,297504,297505,297557,297558,297562,297563,297598,297599,297603,297604,297605,297606,297620,297656,297657,297658,297659,297660,297661,297662,297663,297664,297665,297666,297670,297671,297672,297673,297674,297675,297678,297722,297723,298653,298678,298996,298997,298998,299000,299042,299061,299062,299064,299065,299067,299096,299149,299178,299180,299183,299184,299185,299996,300018,300027,300043,300079,300087,300088,300105,300106,300107,300117,300122,300123,300124,300155,300156,300157,300226,300233,300234,300235,300236,300237,300238,300239,300240,300280,300281,300282,300283,300284,300364,300365,300366,300367,300368,300369,300370,300371,300372,300373,300374,300375,300389,300390,300391,300392,300393,300394,300395,300396,300397,300398,300399,300400,300401,300459,300461,300462,300463,300464,300466,300467,300497,300498,300499,300500,300514,300515,300516,300517,300538,300539,300545,300548,300551,300552,300558,300560,300574,300575,300576,300631,300632,300633,300635,300636,300673,300674,300675,300676,300742,300777,300780,300785,300806,300811,300812,300816,300817,301046,301086,301141,301142,301161,301165,301179,301180,301183,301281,301283,301298,301323,301330,301359,301383,301384,301391,301392,301393,301394,301395,301396,301397,301398,301399,301417,301447,301448,301449,301450,301461,301472,301473,301474,301475,301476,301480,301519,301524,301525,301528,301529,301530,301531,301532,301567,301627,301664,301665,301694,301912,301913,301914,301941,301959,301960,302131,302159,302163,302165,302166,302225,302228,302229,302239,302240,302262,302263,302277,302279,302280,302322,302328,302337,302342,302343,302344,302349,302350,302388,302392,302393,302448,302472,302473,302474,302475,302476,302479,302484,302485,302486,302487,302488,302489,302490,302491,302492,302493,302494,302509,302513,302522,302523,302525,302526,302548,302550,302551,302553,302554,302555,302563,302564,302565,302566,302567,302569,302570,302571,302572,302573,302596,302597,302634,302635,302646,302651,302654,302660,302661,302663,303818,303819,303824,303825,303832,303838,303885,303948,303989,303998,303999,304000,304062,304119,304120,304125,304144,304158,304169,304170,304196,304197,304198,304199,304200,304204,304209,304291,304292,304333,304354,304366,304446,304447,304448,304449,304451,304452,304505,304506,304507,304508,304562,304616,304625,304626,304654,304655,304661,304662,304663,304671,304672,304737,304738,304739,304740,304776,304777,304778,304797,305040,305043,305044,305045,305046,305059,305062,305063,305064,305081,305112,305113,305114,305178,305179,305180,305181,305182,305183,305184,305185,305186,305188,305202,305204,305207,305208,305234,305236,305237,305247,305248,305249,305250,305252,305282,305310,305311,305312,305313,305314,305336,305338,305341,305349,305350,305351,305358,305364,305365,305366,305376,305377,305405,305406,305440,305441,305516,305517,305518,305586,305588,305589,305590,305636,305766,305809,305814,305821,305832,305840,305841,305842,305862,305898,305902,305967,306029,306030,306036,306037,306038,306041,306042,306048,306049,306051,306091,306092,306093,306095,306121,306122,306125,306126,306134,306135,306137,306138,306139,306153,306154,306155,306169,306170,306171,306416,306417,306418,306419,306420,306422,306423,306425,306432,306454,306455,306456,306457,306458,306459,306460,306546,306548,306549,306550,306553,306563,306572,306580,306584,306595,306598,306604,306629,306630,306631,306636,306645,306646,306647,306651,306652,306653,306654,306656,306657]

    for run in listOfRuns:
        print run,print_times(run)[0]

if __name__ == "__main__":        
    main()

