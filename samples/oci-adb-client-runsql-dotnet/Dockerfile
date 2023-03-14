FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add RunSQL.csproj
RUN dotnet build RunSQL.csproj -c Release
RUN dotnet publish RunSQL.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENV TNS_ADMIN=/tmp
ENTRYPOINT ["dotnet", "RunSQL.dll"]
CMD ["RunSQL:Function:function_handler"]