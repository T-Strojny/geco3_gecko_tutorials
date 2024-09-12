from geco3 import corruptor, generator, attrgenfunct, basefunctions
import random
random.seed(42)

unicode_encoding_used = 'utf-8'
rec_id_attr_name = 'rec-id'
out_file_name = 'GECO3_Birthday_test.csv'
num_org_rec = 1000
num_dup_rec = 1000

max_duplicate_per_record = 3
num_duplicates_distribution = 'zipf'
     

max_modification_per_attr = 1
num_modification_per_record = 3
basefunctions.check_unicode_encoding_exists(unicode_encoding_used)

given_name_attr = generator.GenerateFreqAttribute(
                          attribute_name = 'given-name',
                          freq_file_name = 'lookup-files\polish_female_firstnames.csv',
                          has_header_line = True,
                          unicode_encoding = unicode_encoding_used
                          )

surname_attr = generator.GenerateFreqAttribute(
                          attribute_name = 'surname',
                          freq_file_name = 'lookup-files\polish_female_surnames.csv',
                          has_header_line = True,
                          unicode_encoding = unicode_encoding_used
                          )

phone_number_attribute = generator.GenerateFuncAttribute(
                                  attribute_name = 'telephone-number',
                                  function = attrgenfunct.generate_phone_number_poland
                      )

birthday_year = generator.GenerateFuncAttribute(
                                  attribute_name = 'birthday_year',
                                  function = attrgenfunct.generate_birthday_year
                                  )

edit_corruptor2 = corruptor.CorruptValueEdit(
          position_function = corruptor.position_mod_uniform,
          char_set_funct = basefunctions.char_set_ascii,
          insert_prob = 0.25,
          delete_prob = 0.25,
          substitute_prob = 0.25,
          transpose_prob = 0.25
          )


surname_misspell_corruptor = corruptor.CorruptCategoricalValue(
          lookup_file_name = 'lookup-files\misspell_polish_surnames.csv',
          has_header_line = True,
          unicode_encoding = unicode_encoding_used
          )
    
ocr_corruptor = corruptor.CorruptValueOCR(
          position_function = corruptor.position_mod_normal,
          lookup_file_name = 'lookup-files\ocr-variations.csv',
          has_header_line = True,
          unicode_encoding = unicode_encoding_used
          )

missing_val_corruptor = corruptor.CorruptMissingValue()

birthday_year_corruptor = corruptor.CorruptBirthdayYear()


attr_name_list = ['given-name', 'surname','telephone-number',
                  'birthday_year']

attr_data_list = [given_name_attr, surname_attr, phone_number_attribute, birthday_year]

attr_mod_prob_dictionary = {'given-name':0.1,
                            'surname':0.05,
                            'telephone-number':0.05,
                            'birthday_year': 0.8
                            }

attr_mod_data_dictionary = {'surname':[(0.5, surname_misspell_corruptor),
                                       (0.5, ocr_corruptor)],
                            'given-name':[(0.5, edit_corruptor2),
                                          (0.5, ocr_corruptor)],
                            'telephone-number':[(1.0, missing_val_corruptor)],
                            'birthday_year':[(1.0, birthday_year_corruptor)]}


test_data_generator = generator.GenerateDataSet(
                                          output_file_name = out_file_name,
                                          write_header_line = True,
                                          rec_id_attr_name = rec_id_attr_name,
                                          number_of_records = num_org_rec,
                                          attribute_name_list = attr_name_list,
                                          attribute_data_list = attr_data_list,
                                          unicode_encoding = unicode_encoding_used
                                          )

test_data_corruptor = corruptor.CorruptDataSet(number_of_org_records = num_org_rec,
                                                number_of_mod_records = num_dup_rec,
                                                attribute_name_list = attr_name_list,
                                                max_num_dup_per_rec = max_duplicate_per_record,
                                                num_dup_dist = num_duplicates_distribution,
                                                max_num_mod_per_attr = max_modification_per_attr,
                                                num_mod_per_rec = num_modification_per_record,
                                                attr_mod_prob_dict = attr_mod_prob_dictionary,
                                                attr_mod_data_dict = attr_mod_data_dictionary
                                                )

rec_dict = test_data_generator.generate()

assert len(rec_dict) == num_org_rec  # Check the number of generated records

# Corrupt (modify) the original records into duplicate records
#
rec_dict = test_data_corruptor.corrupt_records(rec_dict)

assert len(rec_dict) == num_org_rec+num_dup_rec # Check total number of records

# Write generate data into a file
#
test_data_generator.write()