FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add PutObjects.csproj
RUN dotnet build PutObjects.csproj -c Release
RUN dotnet publish PutObjects.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "PutObjects.dll"]
CMD ["PutObjects:Function:function_handler"]