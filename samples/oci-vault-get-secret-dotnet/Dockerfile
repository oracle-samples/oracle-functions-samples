FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add GetSecrets.csproj
RUN dotnet build GetSecrets.csproj -c Release
RUN dotnet publish GetSecrets.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "GetSecrets.dll"]
CMD ["GetSecrets:Function:function_handler"]