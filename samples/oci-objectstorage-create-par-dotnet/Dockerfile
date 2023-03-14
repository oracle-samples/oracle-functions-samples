FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add CreatePAR.csproj
RUN dotnet build CreatePAR.csproj -c Release
RUN dotnet publish CreatePAR.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "CreatePAR.dll"]
CMD ["CreatePAR:Function:function_handler"]