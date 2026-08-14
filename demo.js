let body = $response.body;

const NEW_XJZT = "\\udbd1\\udd4a\\udbe7\\udf43\\u0028\\udbdb\\ude35\\udbdb\\udc47\\udbe2\\udea7\\udbe7\\udf43\\u0029";
const NEW_BYRQ = "\\udbd3\\udf38\\udbe5\\udc18\\udbd3\\udf38\\udbd5\\udf30\\udbcc\\udddb\\udbe5\\udc18\\udbcf\\ude60\\udbe2\\udff1\\udbd8\\udc09\\udbe5\\udc18\\udbd3\\ude55";

if (body) {
  body = body.replace(/"xjzt":"[^"]*"/, '"xjzt":"' + NEW_XJZT + '"');
  body = body.replace(/"byrq":"[^"]*"/, '"byrq":"' + NEW_BYRQ + '"');
}

$done({ body: body });
