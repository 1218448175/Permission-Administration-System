import JSEncrypt from 'jsencrypt'

// 密钥对生成 http://web.chacuo.net/netrsakeypair

const publicKey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoGyy2uPZjRNY7LoU7R7n\n' +
    '2+9Tc7FhNXsfE9XZ8+ATsH+pb/NjZfBDBb6oJpIHwsO6rMMTQxbfLAa1mAqQmlWF\n' +
    'Mxf8KfhOzT6r8Bfd/AYwUTT+R5pjsW4vDR5IWLSB4afqHj90BDZagV8MwfK7b+fK\n' +
    '9s+9ntDKEoSHT0G0qwW2H+7ApECXbCu1vmP9h/Yke1vANwCnlW6Aawu1owj0TwnE\n' +
    'DiPeCwdTaSNr3ErBrEAgeoGLXnoqcmAvTXCYTmpbHqfRQkMRjfelIv+tcAPNx+A6\n' +
    'Fx7xbZo59kLJC2D2Z9QCbljlu0jKQPTQ+lVE5I9tSmbBTaxAIKJSDErrBMjrsCfb\n' +
    '3wIDAQAB'

const privateKey = 'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCgbLLa49mNE1js\n' +
    'uhTtHufb71NzsWE1ex8T1dnz4BOwf6lv82Nl8EMFvqgmkgfCw7qswxNDFt8sBrWY\n' +
    'CpCaVYUzF/wp+E7NPqvwF938BjBRNP5HmmOxbi8NHkhYtIHhp+oeP3QENlqBXwzB\n' +
    '8rtv58r2z72e0MoShIdPQbSrBbYf7sCkQJdsK7W+Y/2H9iR7W8A3AKeVboBrC7Wj\n' +
    'CPRPCcQOI94LB1NpI2vcSsGsQCB6gYteeipyYC9NcJhOalsep9FCQxGN96Ui/61w\n' +
    'A83H4DoXHvFtmjn2QskLYPZn1AJuWOW7SMpA9ND6VUTkj21KZsFNrEAgolIMSusE\n' +
    'yOuwJ9vfAgMBAAECggEAHgo8s6BW7IPi8vElWgGfiR+XkOJ2QX18pEo3NeOPzE0b\n' +
    'fUsmIcCLzFeXRSGzMlVUb2VYBggSYjwfZQkVatD40Eh9f55vox9JMvxFJRxDj/FM\n' +
    'bDwMzvzC8sHo6jNi3s6CmIdpQiCrce5KhUbesmXFK9Jav5J5RF5st/qlyiCXqgLP\n' +
    'SIWsBY7U9nXfAjaHqAQjWsIOaVTkHR++zvqn8TAk6iQupylymthcsI1AuT0kSeaF\n' +
    'I+zMBoE3VwLnZVi9SnZq2xu3fAVUaqHaOawtFHRmiTyV0sEc2IdE1jSvoBYpPNCn\n' +
    'g8bh4sfCMdulS0zfkuQZbt8xSfagobbvhv/FwHahAQKBgQDNjaFOdO7GJpC9dwCZ\n' +
    '/gF64xrNqq7AKOLlC78bOY6j1wDyLnplEbe/1ot1qSNmYHe2NojZoOKWsRD+Pusr\n' +
    'IoPcUA4/pUgcPBOKC0w6ak9JiPFblZjVuNN5/F88m19N5abel68rPW2ML2O82SEZ\n' +
    'kA//oWKky6G3IINHPoeMx4X1RwKBgQDHy8E8DF9tpZ4RK4uH2Y9vvUFyNhyXfyiQ\n' +
    '3i8AjiLiQPWt4LhzbOMA8oPcEIHpBB42Zfup3ZBVBKENtLWJXjDc4gxhRInPU+8K\n' +
    'dEVJQX+wL/2K19xaBpxsJiv+HxwP7J6UOv9NX3J4qPG3S3gc/q9IHpcJnkQjl4Mx\n' +
    'AFh377eQqQKBgGpIFuWYNHWkLyanx1nYKi++CXfaDu0wttCzWCbdhdFVNBoEyihE\n' +
    'FvxMFGPMBo/CxWMjo3LTaxV7jEvJgJMXD5L0mclyzmw66+dunAWAPmrJMfKm0RWA\n' +
    'sWfbg+q0c3y1h6iESYBUDLZ1Ml7M7f5nrL4CVhzbZUxotTg7Lp8t8ye1AoGAf4gv\n' +
    'E05uh4XlDN631QJpjZDHusiRnZ58XWSFqhwQZk3CxLeh5YPGru8efhVHZ17Kjjyw\n' +
    '1K/qFmq7Bw2np0SpegUMk/X05ZOVDR5Er8sQX31yoPLC4/A+XsZK5I4lEoEehE3Y\n' +
    'cyIO5rgoerDAvflQF3/3NxuAMRvgkSHAVuZ8TOkCgYBOpov1eyUI+BDmcZJkaeES\n' +
    'QCo8o3K+XClt88hAHqUrRO3/ftxDKymGF8FABu4BRjQ7CXabBBuIWmrp4qzZm9O5\n' +
    'N6S+WU8tkB/AmwYeWzWVD1zWNRMw/cN3L0rZLflquXbiR5zzTnm7QnuZo7jfDiCi\n' +
    '0gGow7znTgqVSmlru2rKrQ=='

// 加密
export function encrypt(txt) {
  const encryptor = new JSEncrypt()
  encryptor.setPublicKey(publicKey) // 设置公钥
  return encryptor.encrypt(txt) // 对数据进行加密
}

// 解密
export function decrypt(txt) {
  const encryptor = new JSEncrypt()
  encryptor.setPrivateKey(privateKey) // 设置私钥
  return encryptor.decrypt(txt) // 对数据进行解密
}