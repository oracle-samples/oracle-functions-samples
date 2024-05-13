FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add PublishONS.csproj
RUN dotnet build PublishONS.csproj -c Release
RUN dotnet publish PublishONS.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "PublishONS.dll"]
CMD ["PublishONS:Function:function_handler"]