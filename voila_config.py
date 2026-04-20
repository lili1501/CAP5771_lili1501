c.ServerApp.disable_check_xsrf = True
c.ServerApp.allow_origin = '*'
c.ServerApp.tornado_settings = {'xsrf_cookies': False}
c.VoilaConfiguration.base_url = '/engine/gallery/icu-mortality-prediction-using-first-72-hours-of-mimic-iv-data/'