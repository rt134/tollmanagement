# tollmanagement
GET: /api/leaderboard/ => Get Leaderboard Info
GET: /api/vehicle/<str:vpk>/booth/<int:bpk>/ => Vehicle has Valid Pass or Not. If Not the Shows Price according to the vehicle
POST: /api/vehicle/<str:vpk>/booth/<int:bpk>/ => If the Vehicle doesn't have a pass then Buy it by sending Pass Options, Else Pass the vehicle
