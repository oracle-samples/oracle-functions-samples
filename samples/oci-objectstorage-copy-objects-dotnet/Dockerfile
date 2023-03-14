FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add CopyObjects.csproj
RUN dotnet build CopyObjects.csproj -c Release
RUN dotnet publish CopyObjects.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "CopyObjects.dll"]
CMD ["CopyObjects:Function:function_handler"]