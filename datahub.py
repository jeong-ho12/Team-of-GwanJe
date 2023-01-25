

class Datahub:

    def __init__ (self):

        self.timespace = []
        self.rolls = []
        self.pitchs = []
        self.yaws = []
        self.rollSpeeds = []
        self.pitchSpeeds = []
        self.yawSpeeds = []
        self.Xaccels = []
        self.Yaccels = []
        self.Zaccels = []
        self.latitudes = []
        self.longitudes = []
        self.altitude = []
        
    def update(self,datas):

        self.timespace.append(datas[0])
        self.rolls.append(datas[1])
        self.pitchs.append(datas[2])
        self.yaws.append(datas[3])
        self.rollSpeeds.append(datas[4])
        self.pitchSpeeds.append(datas[5])
        self.yawSpeeds.append(datas[6])
        self.Xaccels.append(datas[7])
        self.Yaccels.append(datas[8])
        self.Zaccels.append(datas[9])
        self.latitudes.append(datas[10])
        self.longitudes.append(datas[11])
        self.altitude.append(datas[12])
