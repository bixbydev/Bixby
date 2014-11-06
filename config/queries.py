
# SIS Queries
# Query pulls all staff from PowerSchool
get_staff_from_sis = """SELECT t.id
					, t.schoolid
					, t.teachernumber
					, CASE WHEN ps_customfields.getcf(\'teachers\',t.id,\'CA_SEID\') IS NOT NULL THEN 1 ELSE 0 END CERTIFICATED
					, t.first_name
					, t.last_name
					, t.middle_name
					, ps_customfields.getcf(\'teachers\',t.id,\'gender\') gender
					, CASE WHEN t.status = 1 THEN 0 ELSE 2 END EXTERNAL_USERSTATUS
					, t.staffstatus STAFF_TYPE
					, CASE WHEN ps_customfields.getcf(\'teachers\',t.id,\'BUSD_NoEmail\')=1 THEN 1
						ELSE 0 END SUSPEND_ACCOUNT
					, CASE WHEN ps_customfields.getcf(\'teachers\',t.id,\'BUSD_Email\')=1 THEN 1
						ELSE 0 END BUSD_Email
					, ps_customfields.getcf(\'teachers\',t.id,\'BUSD_Email_Address\')
					, CASE WHEN ps_customfields.getcf(\'teachers\',t.id,\'CA_SEID\') IS NOT NULL THEN 1
  						ELSE 2 END STAFF_CONFERENCE 
					FROM teachers t
					WHERE t.staffstatus IS NOT NULL
					AND t.schoolid = t.homeschoolid
					AND t.first_name IS NOT NULL -- Remove for Production Version Fix
					AND t.last_name IS NOT NULL  -- Remove for Production Version Fix
					"""

get_students_from_sis = """SELECT id STUDENTID
						, SCHOOLID
						, STUDENT_NUMBER
						, FIRST_NAME
						, LAST_NAME
						, MIDDLE_NAME
						, DOB
						, CASE WHEN UPPER(gender) NOT IN ('M','F') THEN 'U' ELSE UPPER(gender) END GENDER
						, GRADE_LEVEL
						, HOME_ROOM
						, ps_customfields.getcf('students',id,'Area') AREA
						, TO_DATE(entrydate) ENTRYDATE
						, TO_DATE(exitdate) EXITDATE
						, CASE WHEN enroll_status = 0 THEN 0 ELSE 2 END EXTERNAL_USERSTATUS
						, CASE WHEN ps_customfields.getcf('students',id,'BUSD_Gmail_Suspended')=1 THEN 1
							ELSE 0 END SUSPEND_ACCOUNT
						      -- The Student Web ID and Parent Web_ID are here for other purposes maybe I will put that into a custom table
						, NULL EMAIL_OVERRIDE -- Pull from field BUSD_EMAIL_OVERRIDE
						, STUDENT_WEB_ID
						, WEB_ID PARENT_WEB_ID
						FROM students
						-- WHERE id BETWEEN 5000 AND 5200 
						-- AND grade_level >= 3
						ORDER BY id
						"""


# MySQL Queries
insert_staff_py = """INSERT INTO STAFF_PY (STAFFID
						, SCHOOLID
						, TEACHERNUMBER
						, CERTIFICATED
						, FIRST_NAME
						, LAST_NAME
						, MIDDLE_NAME
						, GENDER
						, EXTERNAL_USERSTATUS
						, STAFF_TYPE						
						, SUSPEND_ACCOUNT
						, BUSD_Email
						, BUSD_Email_Address
						, Staff_Conference)
						VALUES(%s, %s, %s, %s, %s
							, %s, %s, %s, %s, %s
							, %s, %s, %s, %s)"""



get_new_staff_accounts = """SELECT sp.staffid EXTERNAL_UID
	, sp.TEACHERNUMBER AS EXTERNAL_USERNUMBER
	, sp.FIRST_NAME
	, sp.LAST_NAME 
	, sp.MIDDLE_NAME
	, UPPER(sp.gender) AS GENDER
	, sp.schoolid AS DEPARTMENT_ID
	, d.DOMAIN_ID
	, ut.USER_TYPEID
	, sp.EXTERNAL_USERSTATUS
	, sp.SUSPEND_ACCOUNT AS SUSPEND_ACCOUNT
	, sp.BUSD_Email_Address AS EMAIL_OVERRIDE_ADDRESS
	, 1 ACCOUNT_STATUS

FROM STAFF_PY AS sp
JOIN USER_TYPES AS ut
	ON ut.user_type = 'Staff'
JOIN DOMAINS AS d
	ON ut.default_domain_id = d.DOMAIN_ID
LEFT JOIN GOOGLE_USERS AS gu
ON sp.STAFFID = gu.EXTERNAL_UID
WHERE sp.SUSPEND_ACCOUNT = 0
	-- AND sp.teachernumber = '3750' -- My Account
	AND gu.LAST_NAME IS NULL
	AND sp.EXTERNAL_USERSTATUS = 0
"""


get_user_info_from_uid = """SELECT FIRST_NAME
						, LAST_NAME
						, MIDDLE_NAME
						, GOOGLE_USERNAME
						, EMAIL_OVERRIDE_ADDRESS
						, DOMAIN_ID 
						FROM GOOGLE_USERS 
						WHERE UID = %s"""



insert_bulk_new_user_accounts = """INSERT INTO GOOGLE_USERS (EXTERNAL_UID
		, EXTERNAL_USERNUMBER
		, FIRST_NAME
		, LAST_NAME
		, MIDDLE_NAME
		, GENDER
		, DEPARTMENT_ID
		, DOMAIN_ID
		, USER_TYPEID
		, EXTERNAL_USERSTATUS
		, SUSPEND_ACCOUNT
		, EMAIL_OVERRIDE_ADDRESS
		, ACCOUNT_STATUS)
(SELECT up.external_uid
, up.EXTERNAL_USERNUMBER
, up.FIRST_NAME
, up.LAST_NAME
, up.middle_name
, up.gender AS GENDER
, up.department_id
, d.DOMAIN_ID
, up.USER_TYPEID
, up.EXTERNAL_USERSTATUS
, up.SUSPEND_ACCOUNT
, up.EMAIL_OVERRIDE
, 1

FROM USERS_PY AS up
JOIN USER_TYPES AS ut
	ON up.user_typeid = ut.USER_TYPEID
JOIN DOMAINS AS d
	ON ut.default_domain_id = d.DOMAIN_ID
LEFT OUTER JOIN GOOGLE_USERS AS gu
	ON up.external_uid = gu.EXTERNAL_UID
		AND ut.user_typeid = gu.USER_TYPEID
WHERE up.SUSPEND_ACCOUNT = 0
	-- AND up.EXTERNAL_USERNUMBER = '3750' -- My Account
	AND gu.uid IS NULL
	AND up.EXTERNAL_USERSTATUS = 0
	-- AND up.USER_TYPEID = 1 -- Remove this limits the new_user creation to staff
	-- AND up.EXTERNAL_UID >= '12288'
-- LIMIT 20
)
"""



insert_bulk_new_staff_accounts = """INSERT INTO GOOGLE_USERS (EXTERNAL_UID
		, EXTERNAL_USERNUMBER
		, FIRST_NAME
		, LAST_NAME
		, MIDDLE_NAME
		, GENDER
		, DEPARTMENT_ID
		, DOMAIN_ID
		, USER_TYPEID
		, EXTERNAL_USERSTATUS
		, SUSPEND_ACCOUNT
		, EMAIL_OVERRIDE_ADDRESS
		, ACCOUNT_STATUS)
	(SELECT sp.staffid EXTERNAL_UID
	, sp.TEACHERNUMBER AS EXTERNAL_USERNUMBER
	, sp.FIRST_NAME
	, sp.LAST_NAME 
	, sp.MIDDLE_NAME
	, UPPER(sp.gender) AS GENDER
	, sp.schoolid AS DEPARTMENT_ID
	, d.DOMAIN_ID
	, ut.USER_TYPEID
	, sp.EXTERNAL_USERSTATUS
	, sp.SUSPEND_ACCOUNT AS SUSPEND_ACCOUNT -- NoEmail
	, sp.BUSD_Email_Address AS EMAIL_OVERRIDE_ADDRESS
	, 1 ACCOUNT_STATUS

FROM STAFF_PY AS sp
JOIN USER_TYPES AS ut
	ON ut.user_type = 'Staff'
JOIN DOMAINS AS d
	ON ut.default_domain_id = d.DOMAIN_ID
LEFT OUTER JOIN GOOGLE_USERS AS gu
ON sp.STAFFID = gu.EXTERNAL_UID
WHERE sp.SUSPEND_ACCOUNT = 0
	AND sp.EXTERNAL_USERSTATUS = 0
	-- AND sp.teachernumber = '3750' -- My Account
	AND gu.LAST_NAME IS NULL

-- LIMIT 1
)"""



insert_bulk_new_student_accounts = """INSERT INTO GOOGLE_USERS (EXTERNAL_UID
		, EXTERNAL_USERNUMBER
		, FIRST_NAME
		, LAST_NAME
		, MIDDLE_NAME
		, GENDER
		, DEPARTMENT_ID
		, DOMAIN_ID
		, USER_TYPEID
		, EXTERNAL_USERSTATUS
		, SUSPEND_ACCOUNT
		, EMAIL_OVERRIDE_ADDRESS
		, ACCOUNT_STATUS)
(SELECT sp.studentid EXTERNAL_UID
	, sp.student_number AS EXTERNAL_USERNUMBER
	, sp.FIRST_NAME
	, sp.LAST_NAME
	, sp.MIDDLE_NAME
	, UPPER(sp.gender) AS GENDER
	, sp.schoolid AS DEPARTMENT_ID
    , d.DOMAIN_ID -- THIS HAS TO BE FIXED FIX-BH
	, ut.USER_TYPEID
	, sp.EXTERNAL_USERSTATUS
	, sp.SUSPEND_ACCOUNT AS SUSPEND_ACCOUNT
	, sp.EMAIL_OVERRIDE AS EMAIL_OVERRIDE_ADDRESS
	, 1 ACCOUNT_STATUS
	-- , ut.USER_TYPE
FROM STUDENTS_PY AS sp
JOIN USER_TYPES AS ut
	ON ut.user_type = 'Student'
JOIN DOMAINS AS d
	ON ut.default_domain_id = d.DOMAIN_ID
LEFT OUTER JOIN GOOGLE_USERS AS gu -- I put Outer here, but it wasn't always there... bad?
ON sp.STUDENTID = gu.EXTERNAL_UID
WHERE sp.SUSPEND_ACCOUNT = 0
	AND sp.EXTERNAL_USERSTATUS = 0
	-- AND sp.teachernumber = '3750' -- My Account
	AND sp.GRADE_LEVEL >= 3
	AND gu.LAST_NAME IS NULL
	
LIMIT 2
)"""


insert_students_py = """INSERT INTO STUDENTS_PY (STUDENTID
											, SCHOOLID
											, STUDENT_NUMBER
											, FIRST_NAME
											, LAST_NAME
											, MIDDLE_NAME
											, DOB
											, GENDER
											, GRADE_LEVEL
											, HOME_ROOM
											, AREA
											, ENTRYDATE
											, EXITDATE
											, EXTERNAL_USERSTATUS
											, SUSPEND_ACCOUNT
											, EMAIL_OVERRIDE
											, STUDENT_WEB_ID
											, PARENT_WEB_ID
											) 
									VALUES (%s, %s, %s, %s, %s
											, %s, %s, %s, %s, %s
											, %s, %s, %s, %s, %s
											, %s, %s, %s)"""




get_new_users = """SELECT gu.uid
						, d.DOMAIN_NAME
						, ut.USER_TYPE
						, gu.FIRST_NAME
						, gu.LAST_NAME
						, gu.EXTERNAL_USERNUMBER
				FROM GOOGLE_USERS AS gu
				JOIN USER_TYPES AS ut
					ON gu.USER_TYPEID = ut.USER_TYPEID
				JOIN DOMAINS AS d
					ON gu.DOMAIN_ID = d.DOMAIN_ID
				WHERE ACCOUNT_STATUS = 1
					-- AND ut.USER_TYPE = %s
				"""

update_username = """UPDATE GOOGLE_USERS
					SET GOOGLE_USERNAME = %s, GOOGLE_PASSWORD = %s, ACCOUNT_STATUS = %s
					WHERE UID = %s"""


get_changed_propper_name = """SELECT gu.UID
, gu.GOOGLE_USERNAME
, gu.LAST_NAME old_lastname
, up.LAST_NAME new_lastname
, gu.FIRST_NAME old_firstname
, up.FIRST_NAME new_firstname
FROM GOOGLE_USERS AS gu
JOIN users_py AS up
	ON gu.EXTERNAL_UID = up.external_uid
		AND gu.USER_TYPEID = up.USER_TYPEID
JOIN USER_TYPES AS ut
	ON up.USER_TYPEID = ut.USER_TYPEID
WHERE gu.ACCOUNT_STATUS < 3
AND gu.EXTERNAL_USERSTATUS = 0
AND gu.SUSPEND_ACCOUNT = 0
AND (gu.LAST_NAME != up.LAST_NAME 
	OR gu.FIRST_NAME != up.FIRST_NAME)
AND ut.USER_TYPE = %s"""

update_propper_name = """UPDATE GOOGLE_USERS SET FIRST_NAME = %s, LAST_NAME = %s WHERE UID = %s"""


get_changed_username = """SELECT uid FROM active_users
WHERE GOOGLE_USERNAME != EMAIL_OVERRIDE_ADDRESS
AND USER_TYPE = %s"""


update_changed_username = """UPDATE GOOGLE_USERS 
	SET GOOGLE_USERNAME = %s
		, EMAIL_OVERRIDE_ADDRESS = %s
	WHERE UID = %s"""




# Orginization Units / Org Units
ou_new_member_count = """SELECT no.new_orgid
							, COUNT(*) newmember_count
							, CEIL(COUNT(*)/25) ITTERATIONS
							, no.new_orgpath
						FROM new_orgmembers AS no
						JOIN GOOGLE_USERS AS gu
						on no.uid = gu.UID
						JOIN DOMAINS AS d
						ON gu.DOMAIN_ID = d.DOMAIN_ID
						WHERE gu.USER_TYPEID = ALL (SELECT USER_TYPEID FROM USER_TYPES WHERE USER_TYPE = %s)
							AND gu.ACCOUNT_STATUS < 3
						GROUP BY no.new_orgid
						, no.new_orgpath"""


ou_new_members = """SELECT no.UID
						, no.new_orgid
						, CONCAT(gu.GOOGLE_USERNAME, '@', d.DOMAIN_NAME) user_name
					FROM new_orgmembers AS no
					JOIN GOOGLE_USERS AS gu
						on no.uid = gu.UID
					JOIN DOMAINS AS d
						ON gu.DOMAIN_ID = d.DOMAIN_ID
					WHERE no.new_orgid = %s
						AND gu.ACCOUNT_STATUS < 3
					"""


ou_update_ou_members = """INSERT INTO ORG_MEMBERS (UID, ORGID) VALUES (%s, %s) 
									ON DUPLICATE KEY
    								UPDATE ORGID = VALUES(ORGID)"""



get_suspended_users = """SELECT gu.uid
-- , gu.LAST_NAME
-- , gu.FIRST_NAME
, gu.GOOGLE_USERNAME
, d.DOMAIN_NAME
, up.EXTERNAL_USERSTATUS
, gu.EXTERNAL_USERSTATUS old_userstatus
, up.SUSPEND_ACCOUNT
, gu.SUSPEND_ACCOUNT old_gmail_suspended
, ut.USER_TYPE
FROM GOOGLE_USERS AS gu
JOIN users_py AS up
	ON gu.EXTERNAL_UID = up.external_uid
		AND gu.USER_TYPEID = up.USER_TYPEID
JOIN DOMAINS AS d
	ON gu.DOMAIN_ID = d.DOMAIN_ID
JOIN USER_TYPES AS ut
	ON gu.USER_TYPEID = ut.USER_TYPEID
WHERE (gu.EXTERNAL_USERSTATUS != up.EXTERNAL_USERSTATUS
OR gu.SUSPEND_ACCOUNT != up.SUSPEND_ACCOUNT)
AND gu.USER_TYPEID = ALL (SELECT USER_TYPEID FROM USER_TYPES WHERE USER_TYPE = %s)
AND gu.ACCOUNT_STATUS < 3
-- AND uid = 19099
"""


update_suspended_user = """UPDATE GOOGLE_USERS 
	SET EXTERNAL_USERSTATUS = %s
	, SUSPEND_ACCOUNT = %s 
	WHERE UID = %s"""

update_account_status = """UPDATE GOOGLE_USERS 
	SET ACCOUNT_STATUS = %s
	WHERE UID = %s"""

# update_deleted_user =


get_group_email_from_id = """SELECT CONCAT(g.GROUP_EMAIL, '@', d.domain_name) email
FROM GROUPS AS g
JOIN DOMAINS AS d
ON g.DOMAIN_ID = d.DOMAIN_ID
WHERE g.GROUPID = %s"""

get_groupid_from_groupemail = """SELECT g.GROUPID
FROM GROUPS AS g
JOIN DOMAINS AS d
ON g.DOMAIN_ID = d.DOMAIN_ID
WHERE g.GROUP_EMAIL = %s"""

get_user_email_from_uid = """SELECT CONCAT(gu.google_username, '@', d.domain_name) email
FROM GOOGLE_USERS AS gu
JOIN DOMAINS AS d
ON gu.DOMAIN_ID = d.DOMAIN_ID
WHERE uid = %s"""


get_uid_from_username = """SELECT uid, GOOGLE_USERNAME FROM active_users WHERE google_username = %s AND user_type = %s"""

update_google_username = """UPDATE google_users SET google_username = %s, EMAIL_OVERRIDE_ADDRESS = %s WHERE uid = %s"""


delete_group_from_groups = """DELETE FROM GROUPS WHERE GROUPID = %s"""




insert_new_group = """INSERT INTO GROUPS ( DEPARTMENT_ID
						, GROUP_EMAIL
						, GROUP_NAME
						, GROUP_DESCRIPTION
						, GROUP_STATUS
						, DOMAIN_ID
						, GROUP_TYPE
						, UNIQUE_ATTRIBUTE)
					VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

