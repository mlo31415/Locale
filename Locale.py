from __future__ import annotations

import re

from Log import Log, LogError

class Locale:
    def __init__(self, rawtext:str):
        self._rawString=""
        self._country=""
        self._state=""
        self._city=""
        self._weirdo=""
        self.Value=rawtext

    def __str__(self) -> str:
        if self._country != "" or self._state != "" or self._city != "":
            return f"{self._country}: {self._state}: {self._city}"
        if self._weirdo != "":
            return self._weirdo
        return self._rawString

    def __eq__(self, other: Locale) -> bool:
        if self._country != "" or self._state != "" or self._city != "" or self._weirdo != "" or \
                other._country != "" or other._state != "" or other._city != "" or other._weirdo != "":
            return self._country == other._country and self._state == other._state and self._city == other._city and self._weirdo == other._weirdo
        return True

    def __hash__(self):
        if self._country != "" or self._state != "" or self._city != "" or self._weirdo != "":
            return hash(self._country)+hash(self._state)+hash(self._city)+hash(self._weirdo)+hash(self._rawString)
        return hash(self._rawString)


    @property
    # Region is the Locale without the city
    def Region(self) -> str:
        if self._country != "" and self._state != "":
            return f"{self._country}:{self._state}"
        if self._country != "":
            return self._country
        if self._state != "":
            return self._state
        if self._weirdo != "":
            return self._weirdo
        return self._rawString

    @property
    def CountryName(self) -> str:
        if self._country != "":
            return self._country
        if self._weirdo != "":  # If there's no country, but there is a weirdo, return it.
            return self._weirdo
        return "US"     # Per Joe, default for no country is US


    @property
    def State(self) -> str:
        return self._state

    @property
    def City(self) -> str:
        return self._city

    # .....................
    @property
    def Value(self) -> str:  # FanzineIssueInfo
        return self._rawString
    @Value.setter
    # Inputs can be:
    #   <country>  (e.g., "US", "U.K.")
    #   <country>:<city>    (e.g., AU: Melbourne)
    #   <State>:<City>      (e.g., IL:Chicago)
    #   US: <city> <state>    (e.g., US: Van Nuys CA)
    def Value(self, val: str) -> None:  # FanzineIssueInfo
        if val is None:
            val=""
        val=val.strip().replace("\n", " ")
        self._rawString=val
        if val == "":
            return

        # Sometimes the Locale is just the name of a country
        JustPlainCountries={
                            "Argentina": "Argentina",
                            "Austria": "Austria",
                            "AT": "Austria",
                            "Australia": "Australia",
                            "AUSTRALIA": "Australia",
                            "AUS": "Australia",
                            "AU": "Australia",
                            "Belgium": "Belgium",
                            "BE": "Belgium",
                            "Brazil": "Brazil",
                            "Canada": "Canada",
                            "CANADA": "Canada",
                            "CA": "Canada",
                            "China": "China",
                            "CH": "China",
                            "CZ": "Czechoslovakia",
                            "Denmark": "Denmark",
                            "DK": "Denmark",
                            "ET": "Eritrea",
                            "France": "France",
                            "FR": "France",
                            "Germany": "Germany",
                            "GE": "Germany",
                            "West Germany": "Germany",
                            "Hong Kong": "Hong Kong",
                            "HK": "Hong Kong",
                            "Ireland": "Ireland",
                            "IE": "Ireland",
                            "Israel": "Israel",
                            "Japan": "Japan",
                            "JP": "Japan",
                            "MX": "Mexico",
                            "Netherlands": "Netherlands",
                            "NL": "Netherlands",
                            "New Zealand": "NZ",
                            "NZ": "NZ",
                            "N. Ireland": "UK",
                            "NI": "UK",
                            "Norway": "Norway",
                            "NO": "Norway",
                            "Poland": "Poland",
                            "PL": "Poland",
                            "Sweden": "Sweden",
                            "SE": "Sweden",
                            "South Africa": "South Africa",
                            "SA": "South Africa",
                            "Switzerland": "Switzerland",
                            "SW": "Switzerland",
                            "SWITZ": "Switzerland",
                            "Turkey": "Turkey",
                            "TK": "Turkey",
                            "UK": "UK",
                            "GB": "UK",
                            "England": "UK",
                            "US": "US",
                            "Venezuela": "Venezuela",
                            "VE": "Venezuela"
                            }
        if val in JustPlainCountries.keys():
            self._country=JustPlainCountries[val]
            return

        # Sometimes the Locale is of the form "Country: <country>
        m=re.match("Country:(.+)$", val)
        if m is not None:
            self._country=m.groups()[0].strip()
            return

        states=['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
        provinces=['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT']
        provincesDict={
            'Alberta': 'AB',
            'British Columbia': 'BC',
            'Manitoba': 'MB',
            'New Brunswick': 'NB',
            'Newfoundland and Labrador': 'NL',
            'Northwest Territories': 'NT',
            'Nova Scotia': 'NS',
            'Nunavut': 'NU',
            'Ontario': 'ON',
            'Prince Edward Island': 'PE',
            'Quebec': 'QC',
            'Saskatchewan': 'SK',
            'Yukon': 'YT'
        }

        def FunnyLetterMatch(pattern: str, s: str) -> list[str] | None:
            # Create a copy of s with all the characters mapped to the casefold() equivalent, but without loss of case
            sfolded=s.casefold()
            assert len(s) == len(sfolded)
            for c, c1 in zip(s, sfolded):
                if c.isupper():
                    c1=c1.upper()
            # Now attempt to match the pattern against sfolded
            m=re.match(pattern, sfolded)
            if m is None:
                return None

            # Create a list of matched strings taken from s
            output=[]
            for i in range(len(m.groups())):
                output.append(s[m.start(i): m.end(i)])

            return output





        # <Country>:<City> <State>
        # First look to see if it is of the form abc: def XX, where XX is two UC letters.
        m=re.match(r"([a-zA-Z\s.]{2,99}):([A-Za-z\s.,-]+) ([A-Z]{2})", val)
        if m:
            self._country=m.groups()[0].strip()
            self._state=m.groups()[2].strip()
            self._city=m.groups()[1].strip()
            return

        out=FunnyLetterMatch(r"([a-zA-Z\s.]{2,99}):([A-Za-z\s.,-]+) ([A-Z]{2})", val)

        # XX:abc, where XX is two UC letters.
        # XX might be a state, province or country code
        m=re.match(r"([A-Z]{2}):([A-Za-z\s.,-]+)", val)
        if m:
            # <Country>: <City>
            # <State>: <City>
            if m.groups()[0] in states:
                self._country="US"
                self._state=m.groups()[0].strip()
                self._city=m.groups()[1].strip()
                return
            elif m.groups()[0] in provinces:
                self._country="CA"
                self._state=m.groups()[0].strip()
                self._city=m.groups()[1].strip()
                return
            else:
                self._country=m.groups()[0].strip()
                self._city=m.groups()[1].strip()
                return

        # Abc XX,  (no colon)
        # XX might be a state, province or country code
        m=re.match(r"([A-Za-z\s.,-]+)[,\s]([A-Z]{2})", val)
        if m:
            first=m.groups()[0].strip()
            second=m.groups()[1].strip()

            if second in states:
                self._country="US"
                self._state=second
                self._city=first
                return
            elif second in provinces:
                self._country="CA"
                self._state=second
                self._city=first
                return
            elif second in JustPlainCountries.keys():
                self._country=JustPlainCountries[second]
                self._city=first
                return
        out=FunnyLetterMatch(r"([A-Za-z\s.,-]+)[,\s]([A-Z]{2})", val)
        i=0

        # <Country>:<City>
        # Abc:Abc where the first token is a known country
        m=re.match(r"([A-Za-z\s]+):([A-Za-z\s.,-]+)", val)
        if m:
            first=m.groups()[0].strip()
            second=m.groups()[1].strip()
            if first in JustPlainCountries.keys():
                self._country=JustPlainCountries[first]
                self._city=second
                return
            elif first in states:
                self._country="US"
                self._state=first
                self._city=second
                return
            elif first in provincesDict.keys():
                self._country="CA"
                self._state=provincesDict[first]
                self._city=second
                return
        out=FunnyLetterMatch(r"([A-Za-z\s]+):([A-Za-z\s.,-]+)", val)
        i=0

        statesTuples=[("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"),
                      ("CT", "Connecticut"), ("DC", "Washington DC"), ("DE", "Delaware"), ("FL", "Florida"), ("GA", "Georgia"),
                      ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"), ("KY", "Kentucky"),
                      ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"),
                      ("MS", "Mississippi"), ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"), ("NH", "New Hampshire"),
                      ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"),
                      ("OK", "Oklahoma"), ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"),
                      ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"),
                      ("WI", "Wisconsin"), ("WY", "Wyoming")]

        # How about a state code or name just stand alone.  E.G., NJ or New Jersey
        if val in states:
            self._country="US"
            self._state=val
            return
        for stup in statesTuples:
            if val == stup[1]:
                self._country="US"
                self._state=stup[0]
                return

        if val == "Multinational" or val == "Various" or val == "various":
            Log(f"ExtractCountry: Can't interpret: '{val}' -- ignored")     # Logged, but not error-logged
            return

        LogError(f"ExtractCountry: Can't interpret: '{val}'")
        self._weirdo=val


    # Unused, so far.
    can_province_names={
        'AB': 'Alberta',
        'BC': 'British Columbia',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'NS': 'Nova Scotia',
        'NT': 'Northwest Territories',
        'NU': 'Nunavut',
        'ON': 'Ontario',
        'PE': 'Prince Edward Island',
        'QC': 'Quebec',
        'SK': 'Saskatchewan',
        'YT': 'Yukon'
    }