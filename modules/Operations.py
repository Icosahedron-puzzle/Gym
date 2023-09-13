import numpy as np
import pandas as pd


class Mining:
    def __init__(self, data: str):
        self.data: str = data
        self.raw_df = pd.read_csv(data)
        self.df: pd.DataFrame = self.load_csv(data)
        # self.filtered_age: pd.DataFrame =
        self._sub_types = np.array(["Both", "Phone", "Email", "Neither"])
        self.sub_df = _
        self.sub_status: dict = self._sub_status()
        self.contact_list = self._contact_list()

    def __str__(self):
        return f"Mining data class for the Lifetime dataset, '{self.data}'"

    def __repr__(self):
        return f"Mining(data={self.data})"

    @staticmethod
    def _get_rows(dataframe: pd.DataFrame, sub_type: str) -> pd.DataFrame:
        return dataframe.loc[(dataframe["Subscribed"] == sub_type)]

    @staticmethod
    def load_csv(filename: str) -> pd.DataFrame:
        df = pd.read_csv(filename)
        filtered_age = df[(df["MemberAge"] > 0) & (df["MemberAge"] < 13)]
        filtered_final = filtered_age[
            (filtered_age.DeliveredEmployee != "Bryan Hill") &
            (filtered_age.DeliveredEmployee != "Shane Haberkorn") &
            (filtered_age.DeliveredEmployee != "Marissa Matthies") &
            (filtered_age.DeliveredEmployee != "Katherine Delamore") &
            (filtered_age.DeliveredEmployee != "Steven Pauka")
            ]
        return filtered_final

    def unsubscribed(self, sub_type: str) -> pd.DataFrame:
        sub_type = str.capitalize(sub_type)
        sub_type_df = self.sub_status[sub_type].copy()
        return sub_type_df

    def family(self, name: str) -> pd.DataFrame:
        return self.df.loc[self.df["ParentName"] == name]

    def _sub_status(self) -> dict:
        df = pd.DataFrame(self.df, copy=True)

        df["Subscribed"] = "Both"
        df.loc[(df["MembershipPhone"] == "Unsubscribed") & (
                df["MembershipEmail"] == "Unsubscribed"), "Subscribed"] = "Neither"
        df.loc[(df["MembershipPhone"] != "Unsubscribed") & (
                df["MembershipEmail"] == "Unsubscribed"), "Subscribed"] = "Phone"
        df.loc[(df["MembershipPhone"] == "Unsubscribed") & (
                df["MembershipEmail"] != "Unsubscribed"), "Subscribed"] = "Email"

        df["Subscribed Cat"] = pd.factorize(df["Subscribed"])[0]
        df_dict: dict = {
            "Both": self._get_rows(df, "Both"),
            "Phone": self._get_rows(df, "Phone"),
            "Email": self._get_rows(df, "Email"),
            "Neither": self._get_rows(df, "Neither")
        }
        self.sub_df = df
        return df_dict

    def _contact_list(self):
        df = self.df.iloc[:, :8]
        return df

    def sub_info(self, sub_type: str):
        # TODO: Add more information.
        if sub_type in self._sub_types:
            return self.sub_status[sub_type].describe()
        else:
            print(
                f"Error: there is no subscription type, '{sub_type}'. You must use one of the following:\n{self._sub_types}. ")
