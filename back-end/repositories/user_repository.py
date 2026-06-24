from core.database import get_connection
import pymysql

class UserRepository:
    def find_by_email(self, email):
        sql = """
            SELECT u.*, cp.company_name, cp.business_registration_no
            FROM users u
            LEFT JOIN company_profiles cp ON u.id = cp.user_id
            WHERE u.email = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (email,))
                return cursor.fetchone()

    def find_by_id(self, user_id):
        sql = """
            SELECT u.id, u.email, u.name, u.role, u.status, u.last_login_at, u.created_at,
                   cp.company_name, cp.business_registration_no, cp.business_type, cp.region_name,
                   cp.is_youth_company, cp.is_woman_company, cp.is_disabled_company, cp.license_codes, cp.license_names,
                   cp.is_verified, cp.verification_status
            FROM users u
            LEFT JOIN company_profiles cp ON u.id = cp.user_id
            WHERE u.id = %s
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id,))
                return cursor.fetchone()

    def create_user_with_company(self, email, password_hash, name, company_name=None, business_registration_no=None):
        user_sql = """
            INSERT INTO users (email, password_hash, name, role)
            VALUES (%s, %s, %s, 'USER')
        """
        company_sql = """
            INSERT INTO company_profiles (user_id, company_name, business_registration_no)
            VALUES (%s, %s, %s)
        """
        with get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(user_sql, (email, password_hash, name))
                    user_id = cursor.lastrowid
                    
                    if company_name or business_registration_no:
                        cursor.execute(company_sql, (user_id, company_name, business_registration_no))
                conn.commit()
                return user_id
            except pymysql.MySQLError as e:
                conn.rollback()
                raise e

    def update_last_login(self, user_id):
        sql = "UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id,))
            conn.commit()

    def update_user_info(self, user_id, name):
        sql = "UPDATE users SET name = %s WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (name, user_id))
            conn.commit()

    def update_password(self, user_id, password_hash):
        sql = "UPDATE users SET password_hash = %s WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (password_hash, user_id))
            conn.commit()

    def update_email(self, user_id, new_email):
        sql = "UPDATE users SET email = %s WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (new_email, user_id))
            conn.commit()

    def update_company_info(self, user_id, company_name, biz_no, biz_type, is_youth, is_woman, is_disabled, licenses):
        # Check if company exists
        check_sql = "SELECT id FROM company_profiles WHERE user_id = %s"
        with get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(check_sql, (user_id,))
                    exists = cursor.fetchone()
                    
                    license_codes = ",".join([lic['code'] for lic in licenses]) if licenses else ""
                    license_names = ",".join([lic['name'] for lic in licenses]) if licenses else ""

                    if exists:
                        update_sql = """
                            UPDATE company_profiles 
                            SET company_name = %s, business_registration_no = %s, business_type = %s,
                                is_youth_company = %s, is_woman_company = %s, is_disabled_company = %s,
                                license_codes = %s, license_names = %s
                            WHERE user_id = %s
                        """
                        cursor.execute(update_sql, (company_name, biz_no, biz_type, is_youth, is_woman, is_disabled, license_codes, license_names, user_id))
                    else:
                        insert_sql = """
                            INSERT INTO company_profiles 
                            (user_id, company_name, business_registration_no, business_type, is_youth_company, is_woman_company, is_disabled_company, license_codes, license_names)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_sql, (user_id, company_name, biz_no, biz_type, is_youth, is_woman, is_disabled, license_codes, license_names))
                conn.commit()
            except pymysql.MySQLError as e:
                conn.rollback()
                raise e

    def update_company_verification(self, user_id, is_verified):
        sql = "UPDATE company_profiles SET is_verified = %s WHERE user_id = %s"
        with get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (is_verified, user_id))
                    if is_verified == 1:
                        role_sql = "UPDATE users SET role = 'COMPANY' WHERE id = %s AND role = 'USER'"
                        cursor.execute(role_sql, (user_id,))
                conn.commit()
            except pymysql.MySQLError as e:
                conn.rollback()
                raise e

    def update_verification_status(self, user_id, status):
        sql = "UPDATE company_profiles SET verification_status = %s WHERE user_id = %s"
        with get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (status, user_id))
                    if status == 'APPROVED':
                        role_sql = "UPDATE users SET role = 'COMPANY' WHERE id = %s AND role = 'USER'"
                        cursor.execute(role_sql, (user_id,))
                conn.commit()
            except pymysql.MySQLError as e:
                conn.rollback()
                raise e

    def get_all_companies_with_users(self):
        sql = """
            SELECT u.id as user_id, u.email, u.name, u.role,
                   cp.company_name, cp.business_registration_no, cp.business_type,
                   cp.is_verified, cp.verification_status, cp.updated_at
            FROM users u
            JOIN company_profiles cp ON u.id = cp.user_id
            ORDER BY cp.updated_at DESC
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = %s"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id,))
            conn.commit()
