using System;

namespace PutObjects
{

    class InputMessage
    {
        public string objectName { get; set; }
        public string bucketName { get; set; }
        public string namespaceName { get; set; }

        public string content { get; set; }

    }

}
