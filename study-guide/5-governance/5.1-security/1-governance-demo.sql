# Dynamic Data Masking (DDM) - w/ masking policies

CREATE MASKING POLICY email_mask AS
(val string) RETURNS string ->
  CASE
    WHEN CURRENT_ROLE() IN ('PAYROLL') THEN val
    ELSE '******'
  END;

ALTER TABLE user_info MODIFY COLUMN email
SET MASKING POLICY email_mask;

# ---------------------------------------------------------
#	conditional masking = column to mask (first arg) + conditional column (second arg)

CREATE MASKING POLICY email_visibility AS
(email varchar, visibility string) RETURNS varchar ->
  CASE
    WHEN CURRENT_ROLE() = 'ADMIN' THEN email
    WHEN VISIBILITY = 'PUBLIC' THEN email				          -- conditional column
    ELSE '***MASKED***'
  END;

ALTER TABLE user_info MODIFY COLUMN email
SET MASKING POLICY email_visibility USING (EMAIL, VISIBILITY);

# ---------------------------------------------------------
#	External Tokenization - w/ external function

CREATE MASKING POLICY email_de_token as
(val string) returns string ->
  case
    when current_role() in ('ANALYST') then de_email(val) 	-- external function!
    else val
  end;

# ---------------------------------------------------------
#	Tag-Based Masking Policies - w/ tags, for columns (not rows)

CREATE TAG governance.tags.accounting;

ALTER TAG governance.tags.accounting SET
   MASKING POLICY account_name_mask,
   MASKING POLICY account_number_mask;

# Protect column data based on the masking policy directly assigned to the tag
ALTER TABLE finance.accounting.name_number
   SET TAG governance.tags.accounting = 'tag-based policies';

# Protect column data based on the column tag string value
ALTER TABLE finance.accounting.name_number MODIFY COLUMN
   account_name SET TAG governance.tags.accounting_col_string = 'visible',
   account_number SET TAG governance.tags.accounting_col_string = 'protect';

# ---------------------------------------------------------
#	Row-Access Policies - for rows, always returns BOOL, on table/view

CREATE ROW ACCESS POLICY rap_it AS
(empl_id varchar) RETURNS BOOLEAN ->
   'it_admin' = current_role();

ALTER TABLE t1
ADD ROW ACCESS POLICY rap_it ON (empl_id);
