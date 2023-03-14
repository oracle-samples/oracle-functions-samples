using Fnproject.Fn.Fdk;

using System.Runtime.CompilerServices;
namespace Function {
	class Greeter {
		public string greet(string input) {
			return string.Format("Hello {0}!",
				string.IsNullOrEmpty(input) ? "World" : input.Trim());
		}

		static void Main(string[] args) { Fdk.Handle(args[0]); }
	}
}
