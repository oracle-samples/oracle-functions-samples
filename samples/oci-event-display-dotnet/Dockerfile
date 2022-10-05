FROM fnproject/dotnet:3.1-1.0.4-dev as build-stage
WORKDIR /function
COPY . .
RUN dotnet sln add LogEvents.csproj
RUN dotnet build LogEvents.csproj -c Release
RUN dotnet publish LogEvents.csproj -c Release -o out
FROM fnproject/dotnet:3.1-1.0.4
WORKDIR /function
COPY --from=build-stage /function/out/ /function/
ENTRYPOINT ["dotnet", "LogEvents.dll"]
CMD ["LogEvents:Function:function_handler"]