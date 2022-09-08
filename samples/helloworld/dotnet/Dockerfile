FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add HelloWorld.csproj
RUN dotnet build HelloWorld.csproj -c Release
RUN dotnet publish HelloWorld.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "HelloWorld.dll"]
CMD ["Function:Greeter:greet"]