#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


holidays = [
    datetime.strptime("1990-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1990-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1990-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1990-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1990-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1990-04-16", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1990-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1990-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1990-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1990-05-24", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1990-06-04", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1991-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1991-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1991-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1991-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1991-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1991-04-01", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1991-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1991-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1991-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1991-05-09", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1991-05-20", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1992-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1992-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1992-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1992-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1992-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1992-04-20", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1992-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1992-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1992-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1992-05-28", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1992-06-08", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1993-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1993-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1993-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1993-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1993-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1993-04-12", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1993-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1993-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1993-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1993-05-20", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1993-05-31", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1994-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1994-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1994-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1994-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1994-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1994-04-04", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1994-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1994-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1994-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1994-05-12", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1994-05-23", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1995-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1995-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1995-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1995-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1995-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1995-04-17", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1995-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1995-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1995-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1995-05-25", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1995-06-05", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1996-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1996-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1996-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1996-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1996-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1996-04-08", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1996-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1996-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1996-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1996-05-16", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1996-05-27", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1997-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1997-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1997-05-08", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1997-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1997-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1997-03-31", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1997-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1997-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1997-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1997-05-19", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1998-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1998-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1998-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1998-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1998-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1998-04-13", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1998-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1998-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1998-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1998-05-21", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1998-06-01", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("1999-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("1999-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("1999-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("1999-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("1999-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("1999-04-05", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("1999-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("1999-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("1999-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("1999-05-13", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("1999-05-24", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2000-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2000-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2000-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2000-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2000-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2000-04-24", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2000-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2000-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2000-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2000-06-01", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2000-06-12", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2001-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2001-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2001-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2001-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2001-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2001-04-16", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2001-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2001-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2001-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2001-05-24", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2001-06-04", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2002-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2002-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2002-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2002-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2002-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2002-04-01", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2002-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2002-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2002-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2002-05-09", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2002-05-20", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2003-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2003-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2003-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2003-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2003-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2003-04-21", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2003-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2003-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2003-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2003-05-29", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2003-06-09", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2004-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2004-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2004-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2004-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2004-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2004-04-12", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2004-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2004-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2004-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2004-05-20", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2004-05-31", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2005-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2005-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2005-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2005-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2005-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2005-03-28", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2005-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2005-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2005-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2005-05-05", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2005-05-16", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2006-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2006-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2006-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2006-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2006-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2006-04-17", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2006-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2006-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2006-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2006-05-25", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2006-06-05", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2007-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2007-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2007-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2007-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2007-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2007-04-09", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2007-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2007-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2007-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2007-05-17", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2007-05-28", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2008-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2008-05-01", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2008-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2008-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2008-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2008-03-24", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2008-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2008-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2008-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2008-05-12", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2009-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2009-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2009-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2009-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2009-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2009-04-13", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2009-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2009-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2009-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2009-05-21", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2009-06-01", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2010-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2010-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2010-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2010-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2010-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2010-04-05", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2010-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2010-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2010-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2010-05-13", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2010-05-24", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2011-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2011-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2011-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2011-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2011-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2011-04-25", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2011-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2011-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2011-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2011-06-02", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2011-06-13", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2012-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2012-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2012-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2012-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2012-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2012-04-09", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2012-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2012-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2012-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2012-05-17", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2012-05-28", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2013-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2013-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2013-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2013-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2013-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2013-04-01", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2013-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2013-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2013-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2013-05-09", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2013-05-20", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2014-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2014-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2014-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2014-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2014-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2014-04-21", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2014-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2014-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2014-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2014-05-29", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2014-06-09", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2015-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2015-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2015-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2015-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2015-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2015-04-06", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2015-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2015-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2015-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2015-05-14", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2015-05-25", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2016-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2016-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2016-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2016-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2016-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2016-03-28", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2016-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2016-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2016-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2016-05-05", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2016-05-16", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2017-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2017-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2017-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2017-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2017-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2017-04-17", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2017-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2017-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2017-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2017-05-25", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2017-06-05", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2018-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2018-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2018-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2018-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2018-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2018-04-02", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2018-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2018-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2018-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2018-05-10", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2018-05-21", "%Y-%m-%d").date(), # Whit Monday
    datetime.strptime("2019-01-01", "%Y-%m-%d").date(), # New year
    datetime.strptime("2019-05-01", "%Y-%m-%d").date(), # Labour Day
    datetime.strptime("2019-05-08", "%Y-%m-%d").date(), # Victory in Europe Day
    datetime.strptime("2019-07-14", "%Y-%m-%d").date(), # Bastille Day
    datetime.strptime("2019-11-11", "%Y-%m-%d").date(), # Armistice Day
    datetime.strptime("2019-04-22", "%Y-%m-%d").date(), # Easter Monday
    datetime.strptime("2019-08-15", "%Y-%m-%d").date(), # Assumption of Mary to Heaven
    datetime.strptime("2019-11-01", "%Y-%m-%d").date(), # All Saints Day
    datetime.strptime("2019-12-25", "%Y-%m-%d").date(), # Christmas Day
    datetime.strptime("2019-05-30", "%Y-%m-%d").date(), # Ascension Thursday
    datetime.strptime("2019-06-10", "%Y-%m-%d").date(), # Whit Monday
    ]
