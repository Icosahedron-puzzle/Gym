import numpy as np
import pandas as pd
from modules.Configuration import GetConfiguration




class Preparation:
    def __init__(self, file_name: str):
        self.config = GetConfiguration("configuration.default.ini")
        self.file_name: str = file_name
        self.raw_df = pd.read_csv(file_name)
        self.rearranged_df = self._rearrange_columns()
        self.df: pd.DataFrame = self.clean_dataframe()
        # self.exported_df = self._email_info_df()

    def __str__(self):
        return f"Data preparation class for Gym dataset, '{self.file_name}'"

    def __repr__(self):
        return f"Preparation(file_name={self.file_name})"

    # @staticmethod
    def clean_dataframe(self) -> pd.DataFrame:
        df = self._rearrange_columns()
        df = self._change_datatypes()
        age_max, age_min = self.config.get_ages()
        att_max, att_min = self.config.get_attendance()
        filtered_age = self._filter_df(df, "Member_Age", lower=age_min, upper=age_max)
        filtered_att = self._filter_df(filtered_age, "Member_Attendance", lower=att_min, upper=att_max)
        filtered_final = self._filter_df(filtered_att, "Engagement_Response_Notes", desc=["Appt/Service Booked", "Not Interested"])
        # filtered_final = filtered_attendance
        return filtered_final

    def _change_datatypes(self):
        df = self.raw_df
        df.Date_Join = df.Date_Join.astype("datetime64[s]")
        df.Date_Member_Birthday = df.Date_Member_Birthday.astype("datetime64[s]")
        df.Date_Activation = df.Date_Activation.astype("datetime64[s]")
        df.Date_Cancellation_Request = df.Date_Cancellation_Request.astype("datetime64[s]")
        df.Date_Expiration = df.Date_Expiration.astype("datetime64[s]")
        df.Date_Member_Most_Recent_Usage = df.Date_Member_Most_Recent_Usage.astype("datetime64[s]")
        df.Date_Package_Create = df.Date_Package_Create.astype("datetime64[s]")
        df.Date_Package_Schedule = df.Date_Package_Schedule.astype("datetime64[s]")
        df.Date_Package_Completion = df.Date_Package_Completion.astype("datetime64[s]")
        df.Date_Engagement = df.Date_Engagement.astype("datetime64[s]")
        return df

    def _rearrange_columns(self):
        col_names = [
            "Member_ID", "Name_Full", "Name_First", "Name_Last", "Member_Sex",
            "Date_Join", "Member_Type", "Membership_Plan", "Membership_Family_Status",
            "Date_Member_DOB", "Member_Age", "Date_Member_Birthday", "DateTime_Created",
            "Date_Activation", "Date_Cancellation_Request", "Date_Expiration",
            "Member_Attendance", "Date_Member_Most_Recent_Usage",
            "Sales_Area_Region", "Sales_Area_State", "Facility_Code", "Engagement_Employee",
            "Date_Package_Create", "Date_Package_Schedule", "Date_Package_Completion",
            "Member_Engagement_ID", "Engagement_ID", "Date_Engagement", "Engagement_Status_ID",
            "Engagement_Response_ID", "Engagement_Employee_ID", "Engagement_Notes",
            "Engagement_Status_Notes", "Engagement_Response_Notes", "Membership_ID",
            "Facility_ID", "Sales_Area_ID"
        ]
        rearranged = [
            "Member_ID", "Name_Full", "Name_First", "Name_Last", "Member_Sex",
            "Member_Age", "Member_Attendance", "Member_Type", "Membership_ID",
            "Membership_Plan", "Membership_Family_Status", "Date_Join", "Date_Member_DOB",
            "Date_Member_Birthday", "DateTime_Created", "Date_Activation",
            "Date_Cancellation_Request", "Date_Expiration", "Date_Member_Most_Recent_Usage",
            "Date_Package_Create", "Date_Package_Schedule", "Date_Package_Completion",
            "Sales_Area_ID", "Sales_Area_Region", "Sales_Area_State", "Facility_ID",
            "Facility_Code", "Engagement_ID", "Member_Engagement_ID",
            "Engagement_Employee_ID", "Engagement_Employee", "Engagement_Status_Notes",
            "Engagement_Notes", "Engagement_Response_Notes", "Engagement_Status_ID",
            "Engagement_Response_ID"
        ]
        self.raw_df.columns = col_names
        dataframe = self.raw_df[rearranged].copy()
        return dataframe

    @staticmethod
    def _filter_df(dataframe: pd.DataFrame, column: str, **kwargs) -> pd.DataFrame:
        """
        Filter a pandas DataFrame based on specified upper and lower bounds for a given column.

        Args:
            dataframe (pd.DataFrame): The DataFrame to be filtered.
            column (str): The name of the column to filter.
            **kwargs: Keyword arguments for specifying filtering conditions.
                - 'upper' (optional): The upper bound for the column values.
                - 'lower' (optional): The lower bound for the column values.

        Returns:
            pd.DataFrame: A filtered DataFrame containing only the rows that satisfy the specified conditions.

        Example:
            # Filter a DataFrame for values in the 'price' column between 10 and 50.
            filtered_data = MyClass._filter_df(dataframe, 'price', upper=50, lower=10)
        """
        if "upper" in kwargs.keys() and "lower" in kwargs.keys():
            return dataframe[(dataframe[column] >= kwargs["upper"]) & (dataframe[column] <= kwargs["lower"])]
        elif "upper" in kwargs.keys() and "lower" not in kwargs.keys():
            return dataframe[dataframe[column] >= kwargs["upper"]]
        elif "upper" not in kwargs.keys() and "lower" in kwargs.keys():
            return dataframe[dataframe[column] <= kwargs["lower"]]
        elif "desc" in kwargs.keys():
            return dataframe[~dataframe[column].isin(kwargs["desc"])]

    def curate(self):
        init_df = self.df
        first_name = init_df.FirstName
        last_name = init_df.LastName
        gender = init_df.Gender
        mem_type = init_df.MemberType
        memship_type = init_df.MembershipTypeProduct
        memship_fam = init_df.MembershipFamilyStatus
        dob = init_df.DOB
        age = init_df.BirthdayAge
        birthday = init_df.BirthdayDate
        attendance = init_df.ClubUsage
        last_attendance = init_df.RecentUsageDate
        ptemployee_name = init_df.PTEmployeeName

        curated_df = pd.DataFrame([])
        return curated_df

    def _email_info_df(self):
        df = self.rearranged_df

