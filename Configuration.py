# Scraping Configuration Section
# 1) Determines which type of houses to be scraped.
# property_start and property_end are the starting and ending indices for the 'properties'
# list given below. They determine the desired property types to scrape.
property_start = 3
property_end = 11
# 2) Determines which states in Malaysia to be scraped
# state_start and state_end are the starting and ending indices for the 'states'
# list given above. They determine the desired states to scrape.
state_start = 0
state_end = 1
# 3) Determines the directory to save the scraped files
directory = r'C:\Users\PH PANG\Desktop\ECON 4200\KL'
# 4) Determines the chromedriver location
driver = r'C:\Users\PH PANG\Desktop\Programmer\chromedriver.exe'


# --------------------------------------------------------------------------
# Appendix
# 1) Determines the type of houses
'''
properties = ['1-sty-terrace-link-house',  #0
              '2-sty-terrace-link-house',  #1
              '3-sty-terrace-link-house',  #2
              '1-5-sty-terrace-link-house',  #3
              '2-5-sty-terrace-link-house',  #4
              '3-5-sty-terrace-link-house',  #5
              '4-5-sty-terrace-link-house',  #6
              '4-sty-terrace-link-house',  #7
              'townhouse',  #8
              'cluster-house',  #9
              'bungalow',  #10
              'semi-detached-house',  #11
              'condominium',  #12
              'apartment',  #13
              'flat'  #14
              ]
'''
# 2) Determines the state in Malaysia
'''
states = ['selangor',  #0
          'kuala-lumpur', #1
          'johor', #2
          'penang',  #3
          'perak',  #4
          'negeri-sembilan', #5
          'pahang', #6
          'melaka', #7
          'sabah', #8
          'sarawak', #9
          'kedah', #10
          'putrajaya', #11
          'kelantan', #12
          'terengganu', #13
          'perlis', #14
          'labuan' #15
          ]
'''
