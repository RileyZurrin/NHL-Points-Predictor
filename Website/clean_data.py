def clean(df):
    # Remove goalie entries
    df = df[df.Pos != "G"]
    # Remove unnecessary columns
    df = df.drop(['Rk','Team'], axis=1)

    # Convert time stats (e.g., 20:12) to seconds.
    # Define function that does the string conversion:
    def time2sec(time):
        m, s = time.split(':')
        return 60 * int(m) + int(s)

    df['TOI'] = df['TOI'].apply(time2sec) 
    df['ES'] = df['ES'].apply(time2sec) 
    df['PP'] = df['PP'].apply(time2sec) 
    df['SH'] = df['SH'].apply(time2sec) 

    # Convert Position to boolean (0 = D, 1 = F)
    def Pos2bool(pos):
        if pos == "D":
            return 0
        if pos == "F":
            return 1
            
    df['Pos'] = df['Pos'].apply(Pos2bool)

    # Remove '%' symbol from columns
    def perc_rem(string):
        return string.replace('%','')

    df['PPP%'] = df['PPP%'].apply(perc_rem)
    df['FO%'] = df['FO%'].apply(perc_rem)
    df['SH%'] = df['SH%'].apply(perc_rem)

    df.set_index("Name")

    return df

def prepare_X(df):
    df = df.fillna(0)
    X = df.values
    return X