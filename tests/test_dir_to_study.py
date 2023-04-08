import pathlib
import orjson
import shutil

from dir_to_study.transform import transform

expected_results = {
    "f4cbc8bbbd5e97722d0b203a1c88a692":
        {"url": "file:///tests/fixtures/file-1.txt", "contentType": "text/plain", "size": 1000000,
         "md5": "f4cbc8bbbd5e97722d0b203a1c88a692"},
    "7823ec49861a566a8a794264b98e89f1":
        {"url": "file:///tests/fixtures/file-2.csv", "contentType": "text/csv", "size": 273,
         "md5": "7823ec49861a566a8a794264b98e89f1"},
    "60b19242b198d6b410ffded7c858222b":
        {"url": "file:///tests/fixtures/sub-dir/file-4.tsv", "contentType": "text/tab-separated-values", "size": 273,
         "md5": "60b19242b198d6b410ffded7c858222b"},
    "2942bfabb3d05332b66eb128e0842cff":
        {"url": "file:///tests/fixtures/sub-dir/file-3.pdf", "contentType": "application/pdf", "size": 13264,
         "md5": "2942bfabb3d05332b66eb128e0842cff"},
    "d6b381911abb6b2e4f417eaf4f5f8365":
        {"url": "file:///tests/fixtures/sub-dir/file-5", "contentType": "text/plain", "size": 5000000,
         "md5": "d6b381911abb6b2e4f417eaf4f5f8365"},
}


# jq '.content[0].attachment | {url: .url, contentType: .contentType, size: .size, md5: .extension[0].valueString}' \
# /tmp/aced-test/DocumentReference.ndjson

def test_simple(output_dir=pathlib.Path('/tmp/aced-test')):
    """Test generated DocumentReferences"""

    if output_dir.is_dir():
        shutil.rmtree(output_dir)

    transform(project_id='aced-test', input_path='./tests/fixtures/', output_path=output_dir, pattern='**/*')

    assert pathlib.Path(output_dir).is_dir(), \
        "Please run: dir_to_study  --project_id aced-test --input_path ./tests/fixtures/ --output_path /tmp/aced-test"

    actual_results = []
    for file_name in pathlib.Path(output_dir).glob("**/*.ndjson"):
        if 'DocumentReference' in str(file_name):
            with open(file_name) as fp:
                for line in fp.readlines():
                    obj = orjson.loads(line)
                    assert obj['resourceType']
                    attachment = obj['content'][0]['attachment']
                    extension = [_ for _ in attachment['extension'] if
                                 _['url'] == "http://aced-idp.org/fhir/StructureDefinition/md5"]
                    assert len(extension) == 1, "Missing MD5 extension."
                    md5 = extension[0]['valueString']
                    assert md5 in expected_results, f"{md5} not in expected_results"
                    expected_result = expected_results[md5]
                    for k in ['url', 'contentType', 'size']:
                        assert attachment[k] == expected_result[k], f"{md5} {k} was not matched"
                    actual_results.append(md5)

                assert len(actual_results) == len(expected_results), "Did not find all files."
