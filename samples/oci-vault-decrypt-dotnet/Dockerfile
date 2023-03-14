FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add VaultDecrypt.csproj
RUN dotnet build VaultDecrypt.csproj -c Release
RUN dotnet publish VaultDecrypt.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "VaultDecrypt.dll"]
CMD ["VaultDecrypt:Function:function_handler"]