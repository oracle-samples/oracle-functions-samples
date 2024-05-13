FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add ListObjects.csproj
RUN dotnet build ListObjects.csproj -c Release
RUN dotnet publish ListObjects.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "ListObjects.dll"]
CMD ["ListObjects:Function:function_handler"]